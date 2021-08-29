from typing import Tuple
from requests_oauthlib import OAuth1, OAuth1Session
import webbrowser

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

    def dance(self):
        """
            Get the access token, save it, and return it
        """
        auth_url = self.get_authorization_url()
        browser_opened = webbrowser.open(auth_url)
        if not browser_opened:
            print('Please open the following URL in a browser:')
            print(auth_url)
        twitter_pin = input('Paste the PIN here: ')
        self.get_access_token(twitter_pin)
        return self.apply_auth()
