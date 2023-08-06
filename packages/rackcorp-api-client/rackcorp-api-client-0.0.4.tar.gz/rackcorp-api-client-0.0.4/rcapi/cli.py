#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import click
from .__init__ import __version__
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from pygments import highlight, lexers, formatters
import click
import pickle
import datetime
import os
import json
from urllib.parse import urlparse
import requests
from requests.auth import AuthBase
import tempfile

import re
import os
import configparser
import pprint
pp = pprint.PrettyPrinter(indent=4)

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
USER_TOKEN = os.getenv("USER_TOKEN")
APIURL = "https://api.rackcorp.net/api/rest/v2.4/json.php"

APIUSER = ""
APIPASS = ""

LOGGING_LEVELS = {
    0: logging.NOTSET,
    1: logging.ERROR,
    2: logging.WARN,
    3: logging.INFO,
    4: logging.DEBUG,
}  #: a mapping of `verbose` option counts to logging levels

class RackCorpConfig:
    def __init__(self, config_file, **kwargs):
        self.config_file = os.path.expanduser(config_file)
        self.config = configparser.ConfigParser()
        self.read()

        self.user = ""
        self.password = ""
        self.token = ""
        self.apiurl = ""
        self.apikey = ""
        self.apisecret = ""


        self.setup()

    def setup(self):
        self.user = self.config.get("rackcorp", "user")
        self.password = self.config.get("rackcorp", "password")
        self.token = self.config.get("rackcorp", "token")
        self.apiurl = self.config.get("api", "url")
        self.apikey = self.config.get("api", "key")
        self.apisecret = self.config.get("api", "secret")

    def create(self):
        temp = tempfile.NamedTemporaryFile()
        self.config.add_section("rackcorp")
        self.config.set("rackcorp", "user", "")
        self.config.set("rackcorp", "password", "")
        self.config.set("rackcorp", "token", "")
        self.config.add_section("api")
        self.config.set("api", "url", "https://api.rackcorp.net/api/rest/v2.4/json.php")
        self.config.set("api", "key", "")
        self.config.set("api", "secret", "")
        self.write()

    def read(self):
        if not os.path.exists(self.config_file):
            self.create()
        with open(self.config_file) as file:
            self.config.read_file(file)
        self.setup()

    def write(self):
        with open(self.config_file, "w") as file:
            self.config.write(file)

    def set(self, section, key, value):
        self.config.set(section, key, value);
        self.write()
        self.setup()

    def get(self, section, key):
        return self.config.get(section, key)
pass_config = click.make_pass_decorator(RackCorpConfig)

class RackCorpAPISession:
    """
    A class to access Rackcorp's API
    """

    def __init__(self,
                 apiKey,
                 apiSecret,
                 config: RackCorpConfig,
                 loginToken='',
                 sessionFileAppendix = '_session.dat',
                 maxSessionTimeSeconds = 15 * 60,
                 proxies = None,
                 userAgent = 'rackcorpPyAPI/0.1',
                 debug = False,
                 forceLogin = False,
                 **kwargs):
        """
        save some information needed to login the session

        you'll have to provide 'loginTestString' which will be looked for in the
        responses html to make sure, you've properly been logged in

        'proxies' is of format { 'https' : 'https://user:pass@server:port', 'http' : ...
        'loginData' will be sent as post data (dictionary of id : value).
        'maxSessionTimeSeconds' will be used to determine when to re-login.
        """
        self.config = config

        urlData = urlparse(config.apiurl)
        self.apiname = urlData.netloc
        self.proxies = proxies
        self.apiKey = apiKey
        self.apiSecret = apiSecret
        self.loginToken = loginToken
        self.baseUrl = config.apiurl
        self.loginUrl = f'{self.baseUrl}?cmd=session.login'
        self.loginTestUrl = f'{self.baseUrl}?cmd=session.iscurrent'
        self.maxSessionTime = maxSessionTimeSeconds
        self.userAgent = 'RackCorpAPI/0.1'
        self.debug = debug

        if config.user != "":
            self.loginUser = config.user
        else:
            self.loginUser = click.prompt("enter user")
            self.config.set("rackcorp", "user", self.loginUser)
        if config.password != "":
            self.loginPass = config.password
        else:
            self.loginPass = ""
        if config.token != "":
            self.loginToken = config.token
        else:
            self.loginToken = ""

        self.sessionFile = os.path.expanduser(f"~/.rcapi_{self.apiname}_{self.loginUser}")

    def modification_date(self, filename):
        """
        return last file modification date as datetime object
        """
        t = os.path.getmtime(filename)
        return datetime.datetime.fromtimestamp(t)

    def login(self, forceLogin = False, **kwargs):
        """
        login to a session. Try to read last saved session from cache file. If this fails
        do proper login. If the last cache access was too old, also perform a proper login.
        Always updates session cache file.
        """
        wasReadFromCache = False
        if self.apiKey and self.apiSecret:
            if self.debug:
                print("api key given, using it instead of login.")

            self.session = requests.Session()
            self.session.headers.update({'user-agent' : self.userAgent, "APIUUID": self.apiKey, "APISECRET": self.apiSecret})
            res = self.session.post(self.loginTestUrl, proxies=self.proxies, **kwargs)
            print(res.text)

            return
        if self.debug:
            print('loading or generating session...')
            print(f"session file is: {self.sessionFile}")
        if os.path.exists(self.sessionFile) and not forceLogin:
            time = self.modification_date(self.sessionFile)
            # only load if file less than 30 minutes old
            lastModification = (datetime.datetime.now() - time).seconds
            if lastModification < self.maxSessionTime:
                with open(self.sessionFile, "rb") as f:
                    self.session = pickle.load(f)
                    wasReadFromCache = True
                    if self.debug:
                        print("loaded sessionId %s from cache (last access %ds ago) "
                              % (self.session.params['sessionId'], lastModification))

        if not wasReadFromCache:
            self.session = requests.Session()
            self.session.headers.update({'user-agent' : self.userAgent})

            if self.loginUser == "":
                if config.user:
                    self.loginUser = config.user
                else:
                    self.loginUser = prompt(f"enter username: ")
            if self.loginUser != "":
                if self.loginPass == "":
                    self.loginPass = click.prompt(f"enter password for {self.loginUser}: ", hide_input=True)
            if self.loginUser != "" and self.loginPass != "" and self.loginToken != '':
                self.loginToken = click.prompt(f"Enter 2FA code for {self.loginUser}@{self.apiname}")

            queryString = {'cmd': 'session.login',
                           'serviceProviderCustomerId': '1',
                            'username': self.loginUser,
                            'password': self.loginPass}
            if self.loginToken != '':
                queryString['2fatoken'] = self.loginToken
            res = self.session.post(self.loginUrl, json=queryString, proxies = self.proxies, **kwargs)

            loginInfo = res.json()
            if loginInfo:
                if loginInfo['code']:
                    if loginInfo['code'] == "OK":
                        self.session.params['sessionId'] = loginInfo['sessionId']
                    else:
                        if loginInfo['fault']:
                            if loginInfo['fault']['faultstring']:
                                raise Exception(f"{loginInfo['fault']['faultcode']} error: {loginInfo['fault']['faultstring']}")
                            else:
                                raise Exception(f"server fault: {loginInfo}")
                        else:
                            raise Exception(f"login failed: {loginInfo['message']}")
            else:
                raise Exception("login failed. please check your credentials.")

            if self.debug:
                print('created new session with login' )
            self.saveSessionToCache()

        # test login
        res = self.session.get(self.loginTestUrl)
        data = res.json()
        if data['userstatus'] is False:
            raise Exception("could not log into API (valid session not found)")

    def saveSessionToCache(self):
        """
        save session to a cache file
        """
        # always save (to update timeout)
        self.sessionFile = os.path.expanduser(f"~/.rcapi_{self.apiname}_{self.loginUser}")
        print(f"writing to {self.sessionFile}")
        with open(self.sessionFile, "wb") as f:
            pickle.dump(self.session, f)
            if self.debug:
                print('updated session cache-file %s' % self.sessionFile)

    def cmd(self, cmd, params={}):
        params['cmd'] = cmd
        return self.exec(params)

    def exec(self, data, **kwargs):
        if self.apiKey and self.apiSecret:
            data['APIUUID'] = self.apiKey
            data['APISECRET'] = self.apiSecret
        else:
            data['USERSESSIONID'] = self.session.params['sessionId']

        if self.debug:
            pp.pprint(f"executing: {data}")


        res = self.session.post(self.baseUrl, json=data, proxies = self.proxies, **kwargs)
        rdata = res.json()
        loginInfo = res.json()
        if rdata:
            if rdata['code']:
                if rdata['code'] == "OK":
                    return rdata
                else:
                    if rdata['fault']:
                        if rdata['fault']['faultstring']:
                            raise Exception(
                                f"{rdata['fault']['faultcode']} error: {rdata['fault']['faultstring']}")
                        else:
                            raise Exception(f"server fault: {rdata}")
                    else:
                        raise Exception(f"execution failed: {rdata['message']}")
        else:
            if self.debug:
                print(res)
            raise Exception("something went wrong.")
        return rdata
pass_api = click.make_pass_decorator(RackCorpAPISession)

class GetSet(click.ParamType):
    """A basic object to check API Keys are legit."""
    name = 'get-set'

    def convert(self, value, param, ctx):
        found = re.match(r'[gs]et', value)

        if not found:
            self.fail(
                f'valid options are [get/set]',
                param,
                ctx,
            )

        return value

class ApiKey(click.ParamType):
    """A basic object to check API Keys are legit."""
    name = 'api-key'

    def convert(self, value, param, ctx):
        found = re.match(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', value)

        if not found:
            self.fail(
                f'{value} is not a 32-character hexadecimal string',
                param,
                ctx,
            )

        return value

@click.group()
@click.option("--verbose", "-v", count=True, help="Enable verbose output.")
@click.option("--pretty", "-p", count=True, help="Enable pretty output.")
@click.option(
    '--api-key', '-a',
    type=ApiKey(),
    help='RackCorp API Key',
    default=API_KEY
)
@click.option(
    '--api-secret', '-s',
    type=str,
    help='RackCorp API Secret',
    default=API_SECRET
)
@click.option(
    '--token', '-t',
    type=str,
    help='2FA Token for use with user authentication',
    default=USER_TOKEN
)
@click.option(
    '--config-file', '-c',
    type=click.Path(),
    default='~/.rcapi',
    help='RackCorp config file (default ~/.rcapi)',
)
@click.pass_context
def cli(ctx, verbose: int, pretty: int, api_key, api_secret, token, config_file):
    """Run rackcorp api commands."""
    # Use the verbosity count to determine the logging level...
    if verbose > 0:
        logging.basicConfig(
            level=LOGGING_LEVELS[verbose]
            if verbose in LOGGING_LEVELS
            else logging.DEBUG
        )
        click.echo(
            click.style(
                f"Verbose logging is enabled. "
                f"(LEVEL={logging.getLogger().getEffectiveLevel()})",
                fg="yellow",
            )
        )

    ctx.config = RackCorpConfig(config_file)
    ctx.api_key = ctx.config.apikey
    ctx.api_secret = ctx.config.apisecret
    if api_key:
        ctx.api_key = api_key
    if api_secret:
        ctx.api_secret = api_secret
    ctx.api = RackCorpAPISession(ctx.api_key, ctx.api_secret, config=ctx.config, debug=verbose, loginToken=token)
    ctx.obj = {"config_file": config_file,
               "config": ctx.config,
               "api": ctx.api,
               "pretty": pretty,
               "verbose": verbose}


@cli.command()
@click.pass_context
@click.option('--section', '-s', default="rackcorp", help="section to write to (e.g rackcorp or api)")
@click.argument('operation', type=GetSet(), default="get")
@click.argument('key', default="all")
@click.argument('value', required=False)
def config(ctx, section, operation, key, value):
    """Setup configuration values"""

    config = ctx.obj['config']
    if operation == "get":
        # obfuscated sensitive values for console output
        config = dict(config.config.items(section))
        if 'pass' in config and config['pass' != ""]:
            config['pass'] = "obfuscated"
        if 'password' in config and config['password'] != "":
            config['password'] = "obfuscated"
        if 'secret' in config and config['secret'] != "":
            config['secret'] = "obfuscated"
        if key == "all":
            pp.pprint(config)
        else:
            result = config.get(section, key)
            return result
    if operation == "set":
        if key == "all":
            raise Exception("key/value is required when setting")
        else:
            result = config.set(section, key, value)
            return result

@cli.command()
def version():
    """Get the current library version."""
    click.echo(click.style(f"{__version__}", bold=True))

@cli.command()
@click.argument('command', nargs=1)
@click.pass_context
def exec(ctx, command, *args):
    """Execute a simple command with no arguments"""
    s = ctx.obj['api']
    try:
        s.login()
    except Exception as e:
        click.echo(f"FAIL: {e}")
        return

    js = {"cmd": command}
    try:
        result = s.exec(js)
    except Exception as e:
        click.echo(f"FAIL: {e}")
        return

    if ctx.obj['pretty'] > 0:
        formatted_json = json.dumps(result, sort_keys=True, indent=4)
        colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
        click.echo(colorful_json)
    else:
        click.echo(json.dumps(result))

@cli.command()
@click.option('--operator', '-o', default='=', help="change the split operator")
@click.argument('input', nargs=-1)
@click.pass_context
def do(ctx, input, operator, *args):
    """Execute commands by entering key/value strings.

        This will parse each input argument and split it by an operator (default =).\n
        Multiple arguments can be given.

        Example inputs\n
            cmd=device.get deviceId=1\n
            cmd=session.iscurrent sessionId=<SESSION_ID>
            """
    s = ctx.obj['api']
    try:
        s.login()
    except Exception as e:
        click.echo(f"FAIL: {e}")
        return

    cmd = {}
    for args in input:
        key, value = args.split(operator)
        cmd[key] = value

    try:
        result = s.exec(cmd)
    except Exception as e:
        click.echo(f"FAIL: {e}")
        return

    if ctx.obj['pretty'] > 0:
        formatted_json = json.dumps(result, sort_keys=True, indent=4)
        colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
        click.echo(colorful_json)
    else:
        click.echo(json.dumps(result))

