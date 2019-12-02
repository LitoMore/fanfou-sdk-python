# -*- coding: utf-8 -*-

import requests
from . import oauth


class Fanfou:
    def __init__(
        self,
        consumer_key='',
        consumer_secret='',
        oauth_token='',
        oauth_token_secret='',
        username='',
        password='',
        api_domain='api.fanfou.com',
        oauth_domain='fanfou.com',
        protocol='https:',
        hooks={
            'base_string': lambda str: str
        }
    ):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        self.username = username
        self.password = password
        self.api_domain = api_domain
        self.oauth_domain = oauth_domain
        self.protocol = protocol
        self.hooks = hooks
        self.oauth_init()
        self.api_init()

    def oauth_init(self):
        self.hash_function = lambda key, base_string: oauth.hmacsha1(
            key, base_string)
        self.params_separator = ','
        self.signature_medtod = 'HMAC-SHA1'
        self.o = oauth.OAuth(
            consumer={
                'key': self.consumer_key,
                'secret': self.consumer_secret
            },
            signature_method='HMAC-SHA1',
            parameter_seperator=',',
            hash_function=lambda base_string, key: oauth.hmacsha1(
                base_string, key)
        )
        return self

    def api_init(self):
        self.api_endpoint = self.protocol + '//' + self.api_domain
        self.oauth_endpoint = self.protocol + '//' + self.oauth_domain
        return self

    def xauth(self):
        url = self.oauth_endpoint + '/oauth/access_token'
        params = {
            'x_auth_mode': 'client_auth',
            'x_auth_password': self.password,
            'x_auth_username': self.username
        }
        authorization = self.o.get_authorization(
            self.o.authorize({'url': url, 'method': 'POST'}))
        r = requests.post(
            url,
            headers={
                'Authorization': authorization,
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data=params
        )
        return r.text

    def get(self, uri, params):
        print(uri)

    def post(self, uri, params):
        print(uri)
