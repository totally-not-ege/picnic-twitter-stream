from typing import Tuple
import requests
from requests_oauthlib import OAuth1, OAuth1Session
import webbrowser

class _AuthData:
    auth_file_path = ".authfile"

    @classmethod
    def get(cls) -> Tuple[str, str]:
        try:
            auth_file = open(cls.auth_file_path, "r")
            auth_data = auth_file.read().split("\n")
            acces_token = auth_data[0]
            acces_token_secret = auth_data[1]
            return (acces_token, acces_token_secret)
        except FileNotFoundError:
            return None, None

    @classmethod
    def set(cls, acces_token: str, acces_token_secret: str):
        try:
            auth_file = open(cls.auth_file_path, "w")
            auth_file.write(acces_token + "\n" + acces_token_secret)
        except FileNotFoundError:
            return None

class OAuthDancer:
    """OAuth authentication handler"""
    AUTH_BASE_URL = 'https://api.twitter.com/oauth/'

    def __init__(self, client_key: str, client_secret: str):
        """
        Responsible for authanticating with Twitter

        Args:
            client_key (str): Twitter API key
            client_secret (str): Twitter API secret
        """
        self.client_key = client_key
        self.client_secret = client_secret
        self.access_token = None
        self.access_token_secret = None
        self.request_token = {}
        self.oauth = OAuth1Session(client_key,
                                   client_secret=client_secret)

    def _get_oauth_url(self, endpoint:str) -> str:
        return self.AUTH_BASE_URL + endpoint

    def apply_auth(self) -> OAuth1:
        return OAuth1(self.client_key,
                      client_secret=self.client_secret,
                      resource_owner_key=self.access_token,
                      resource_owner_secret=self.access_token_secret)

    def _get_request_token(self):
        url = self._get_oauth_url('request_token')
        return self.oauth.fetch_request_token(url)

    def get_authorization_url(self) -> str:
        """Get the authorization URL to redirect the user"""
        url = self._get_oauth_url('authorize')
        self.request_token = self._get_request_token()
        return self.oauth.authorization_url(url)

    def get_access_token(self, verifier) -> Tuple[str, str]:
        """
        After user has authorized the request token, get access token
        with user supplied verifier.
        """
        if not verifier: raise Exception('Verifier required')
        url = self._get_oauth_url('access_token')
        self.oauth = OAuth1Session(self.client_key,
                                    client_secret=self.client_secret,
                                    resource_owner_key=self.request_token['oauth_token'],
                                    resource_owner_secret=self.request_token['oauth_token_secret'],
                                    verifier=verifier)
        resp = self.oauth.fetch_access_token(url)
        self.access_token = resp['oauth_token']
        self.access_token_secret = resp['oauth_token_secret']
        return self.access_token, self.access_token_secret
    
    def _load_existing_token(self):
        self.access_token, self.access_token_secret = _AuthData.get()
        return self.access_token is not None and self.access_token_secret is not None

    def _save_token(self):
        _AuthData.set(self.access_token, self.access_token_secret)

    def check_auth(self, auth_object: OAuth1):
        r = requests.request("GET", "https://api.twitter.com/1.1/account/verify_credentials.json", auth=auth_object)
        return r.status_code == 200

    def dance(self):
        """
            Get the access token, save it, and return it
        """
        if self._load_existing_token():
            auth_object = self.apply_auth()
            if self.check_auth(auth_object):
                return auth_object
        auth_url = self.get_authorization_url()
        browser_opened = webbrowser.open(auth_url)
        if not browser_opened:
            print('Please open the following URL in a browser:')
            print(auth_url)
        twitter_pin = input('Paste the PIN here: ')
        self.get_access_token(twitter_pin)
        self._save_token()
        return self.apply_auth()
