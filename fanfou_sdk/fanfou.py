# -*- coding: utf-8 -*-

import requests
from six.moves.urllib import parse
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
        protocol='http:',
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
        self.signature_method = 'HMAC-SHA1'
        self.o = oauth.OAuth(
            consumer={
                'key': self.consumer_key,
                'secret': self.consumer_secret
            },
            signature_method='HMAC-SHA1',
            parameter_seperator=',',
            hash_function=lambda base_string, key: oauth.hmacsha1(
                self.hooks['base_string'](base_string), key)
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
        if (r.status_code != 200):
            return None, r
        token = parse.parse_qs(r.text)
        self.oauth_token = token['oauth_token'][0]
        self.oauth_token_secret = token['oauth_token_secret'][0]
        return {'oauth_token': self.oauth_token, 'oauth_token_secret': self.oauth_token_secret}, r

    def get(self, uri, params={}):
        url = self.api_endpoint + uri + '.json'
        if bool(params):
            url += '?%s' % parse.urlencode(params)
        token = {'key': self.oauth_token, 'secret': self.oauth_token_secret}
        authorization = self.o.get_authorization(
            self.o.authorize({'url': url, 'method': 'GET'}, token=token))
        r = requests.get(
            url,
            headers={
                'Authorization': authorization,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )
        if (r.status_code != 200):
            return None, r
        return r.json(), r

    def post(self, uri, params={}, files=None):
        url = self.api_endpoint + uri + '.json'
        token = {'key': self.oauth_token, 'secret': self.oauth_token_secret}
        is_upload = uri in ['/photos/upload', '/account/update_profile_image']
        authorization = self.o.get_authorization(self.o.authorize(
            {'url': url, 'method': 'POST', 'data': {} if is_upload else params}, token=token))
        headers = {
            'Authorization': authorization,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        if is_upload:
            del headers['Content-Type']
        r = requests.post(
            url,
            headers=headers,
            data=params,
            files=files
        )
        if(r.status_code != 200):
            return None, r
        return r.json(), r
