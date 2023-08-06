from http.server import BaseHTTPRequestHandler, HTTPServer
from dataclasses import dataclass
from webbrowser import open_new
from typing import Any
import shutil
import os

from requests.exceptions import ConnectionError, HTTPError
from arrow import get as _, utcnow
import requests

from tokko_cli.repos import clone_monorepo
from tokko_cli.conf import Settings
from tokko_cli.utils import render
from tokko_cli.templates import (
    SUCCESS_GITHUB_LOGIN_TEMPLATE as SUCCESS_TEMPLATE
)

TREE_DOTS_SPACER = "\t...\t"
OK = "OK"
PORT = 9141
HOST = 'localhost'
REDIRECT_URL = f'http://{HOST}:{PORT}'
REQUIRED_SCOPES = ""
CLIENT_ID = "Iv1.0d575eabb0a7cddf"
CLIENT_SECRET = "a065c6d353f81a1ad05edea4894cfe715b8d8936"


def get_access_token_from_url(url):
    """
    Parse the access token from GitHub's response
    Args:
        url: the facebook graph api oauth URI containing valid client_id,
             redirect_uri, client_secret, and auth_code arguments
    Returns:
        a string containing the access key
    """
    try:
        res = requests.get(url)
        res.raise_for_status()
        return {e.split("=")[0]: e.split("=")[1] for e in res.text.split("&")}
    except ConnectionError:
        raise IOError("Connection Error!")
    except HTTPError as http_error:
        print(http_error)
        raise IOError(f"HttpError. {http_error}")


class HTTPServerHandler(BaseHTTPRequestHandler):
    auth_token = None
    tokens = None

    def __init__(self, request, address, server, a_id, a_secret):
        self.app_id = a_id
        self.app_secret = a_secret
        super().__init__(request, address, server)

    def do_GET(self):
        GRAPH_API_AUTH_URI = (f'https://github.com/login/oauth/access_token?'
                              f'client_id={self.app_id}&'
                              f'redirect_uri={REDIRECT_URL}&'
                              f'client_secret={self.app_secret}&'
                              f'code=')
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        if 'code' in self.path:
            self.auth_token = self.path.split('=')[1]
            # Display to the user that they no longer need the browser window
            self.wfile.write(bytes(render(SUCCESS_TEMPLATE), 'utf-8'))
            tokens = get_access_token_from_url(GRAPH_API_AUTH_URI + self.auth_token)
            setattr(self.server, "tokens", tokens)


class TokenHandler:
    """
    Class used to handle Github oAuth
    """
    @dataclass
    class Token:
        access_token: str
        token_type: str
        expires_in: str
        refresh_token: str
        refresh_token_expires_in: str
        scope: str

        __created_at__ = utcnow().to("local")

        def token_expiration(self):
            return _(self.__created_at__).shift(seconds=float(self.expires_in))

        def refresh_token_expiration(self):
            return _(self.__created_at__).shift(seconds=float(self.refresh_token_expires_in))

    __token__ = None

    def __init__(self, a_id, a_secret):
        self._id = a_id
        self._secret = a_secret

    def get_access_token(self):
        ACCESS_URI = (f"https://github.com/login/oauth/authorize?"
                      f"client_id={self._id}&"
                      f"redirect_uri={REDIRECT_URL}&"
                      f"scope={REQUIRED_SCOPES}")

        open_new(ACCESS_URI)
        httpServer = HTTPServer(
            (HOST, PORT),
            lambda rqt, addr, srv: HTTPServerHandler(
                rqt, addr, srv, self._id, self._secret
            ))
        # This function will block until it receives a request
        httpServer.handle_request()
        # Return the access token
        return httpServer.tokens

    @property
    def auth_credentials(self) -> Token:
        if not self.__token__:
            self.__token__ = self.get_access_token()
        return self.Token(**self.__token__)


def update_config(user: str, section: str, entry: str, value: Any):
    settings = Settings(current_user=user)
    getattr(settings, section).update(entry, value)


def login_with_github(user: str):
    """ Login {user} into github and update tokkoCLI settings"""
    print("Connecting with github", end=TREE_DOTS_SPACER, flush=True)
    user_tokens = TokenHandler(CLIENT_ID, CLIENT_SECRET).auth_credentials
    update_config(user, "user", "github_refresh_token",
                  user_tokens.refresh_token)
    update_config(user, "user", "refresh_token_expiration",
                  f"{user_tokens.refresh_token_expiration()}")
    print(OK)
    return user_tokens.access_token


def create_sources_folder(user: str):
    print(f"Creating {user} sources folder", end=TREE_DOTS_SPACER)
    src_folder = os.path.join("/home", user, "tokko/sources/services-tokkobroker")
    os.makedirs(src_folder, 0o750, exist_ok=True)
    update_config(user, "sources", "monorepo_path", src_folder)
    print(OK)


def fix_user_permission(user: str):
    print(f"Fixing {user}'s sources folder permission", end=TREE_DOTS_SPACER)
    shutil.chown(f'/home/{user}/tokko', user=user, group=user)
    print(OK)


def initialize_user(user: str):
    create_sources_folder(user)
    access_token = login_with_github(user)
    # print(f"Github token {access_token}")
    clone_monorepo(user, access_token)
    fix_user_permission(user)
    update_config(user, "cli", "is_initialized", "True")
    settings = Settings(current_user=user)
    return {
        "user": user,
        "github": {},
        "settings": settings
    }
