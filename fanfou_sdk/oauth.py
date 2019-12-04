# -*- coding: utf-8 -*-

import six
import time
import hmac
import random
import hashlib
import binascii
from six.moves.urllib import parse


def hmacsha1(base_string, key):
    hash = hmac.new(key.encode(), base_string.encode(), hashlib.sha1)
    return binascii.b2a_base64(hash.digest())[:-1]


class OAuth(object):
    def __init__(
        self,
        consumer={},
        nonce_length=32,
        version='1.0',
        parameter_seperator=', ',
        realm='',
        last_ampersand=True,
        signature_method='HMAC-SHA1',
        hash_function=lambda base_string, key: key,
        body_hash_function=lambda base_string, key: key
    ):
        self.consumer = consumer
        self.nonce_length = nonce_length
        self.version = version
        self.parameter_seperator = parameter_seperator
        self.realm = realm
        self.last_ampersand = last_ampersand
        self.signature_method = signature_method
        self.hash_function = hash_function
        self.body_hash_function = body_hash_function

    def authorize(self, request, token={}):
        oauth_data = {
            'oauth_consumer_key': self.consumer['key'],
            'oauth_signature_method': 'HMAC-SHA1',
            'oauth_timestamp': str(int(time.time())),
            'oauth_nonce': ''.join([str(random.randint(0, 9)) for _ in range(8)]),
            'oauth_version':  '1.0'
        }
        if 'key' in token:
            oauth_data['oauth_token'] = token['key']
        if 'data' not in request:
            request['data'] = {}
        if 'include_body_hash' in request:
            oauth_data['oauth_body_hash'] = ''
        oauth_data['oauth_signature'] = self.get_signature(
            request, token.get('secret', ''), oauth_data)
        return oauth_data

    def get_authorization(self, oauth_data):
        authorization = 'OAuth '
        if self.realm != '':
            authorization += 'realm="%s"' % self.realm
            authorization += self.parameter_seperator
        for k, v in sorted(oauth_data.items()):
            if k.startswith('oauth_') or k.startswith('x_auth_'):
                authorization += '%s="%s"%s' % (k,
                                                self.escape(v), self.parameter_seperator)
        return authorization[:-1]

    def get_signature(self, request, token_secret, oauth_data):
        return self.hash_function(self.get_base_string(request, oauth_data), self.get_signing_key(token_secret))

    def get_query(self, args, via='quote', safe='~'):
        return '&'.join('%s=%s' % (k, self.escape(v, via, safe)) for k, v in sorted(args.items()))

    def get_base_string(self, request, oauth_data):
        query = parse.urlparse(request['url'])[4:-1][0]
        params = {}
        for k, v in parse.parse_qs(query).items():
            params[k] = v[0]
        params.update(request['data'])
        oauth_data.update(params)
        base_elements = (request['method'].upper(), self.normalized_url(
            request['url']), self.get_query(oauth_data))
        base_string = '&'.join(self.escape(s) for s in base_elements)
        return base_string

    def get_signing_key(self, token_secret=''):
        if (self.last_ampersand == False) & (token_secret == ''):
            return self.escape(self.consumer['secret'])
        return self.escape(self.consumer['secret']) + '&' + self.escape(token_secret)

    def escape(self, s, via='quote', safe='~'):
        quote_via = getattr(parse, via)
        if isinstance(s, (int, float)):
            s = str(s)
        if not isinstance(s, six.binary_type):
            s = s.encode('utf-8')
        return quote_via(s, safe=safe)

    def normalized_url(self, url):
        scheme, netloc, path = parse.urlparse(url)[:3]
        return '{0}://{1}{2}'.format(scheme, netloc, path)
