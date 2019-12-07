# fanfou-sdk-python

[![](https://github.com/LitoMore/fanfou-sdk-python/workflows/CI/badge.svg)](https://github.com/LitoMore/fanfou-sdk-python/actions)
[![](https://img.shields.io/pypi/v/fanfou-sdk)](https://pypi.org/project/fanfou-sdk)
[![](https://img.shields.io/pypi/l/fanfou-sdk)](https://github.com/LitoMore/fanfou-sdk-python/blob/master/LICENSE)

Fanfou SDK for Python

## Install

```bash
$ pip install fanfou_sdk
```

---

<a href="https://www.patreon.com/LitoMore">
  <img src="https://c5.patreon.com/external/logo/become_a_patron_button@2x.png" width="160">
</a>

## Usage

### OAuth

```python
from fanfou_sdk import Fanfou

ff = Fanfou(
    consumer_key='',
    consumer_secret='',
    oauth_token='',
    oauth_token_secret=''
)

result, response = ff.get('/statuses/home_timeline', {'format': 'html'})
print(result, response)
```

### XAuth

```python
ff = Fanfou(
  consumer_key='',
  consumer_secret='',
  username='',
  password=''
)

token, response = ff.xauth()
print(token, response)

timeline, _ = ff.get('/statuses/public_timeline', {'count': 10})
print(timeline)

status, _ = ff.post('/statuses/update', {'status': 'Hi Fanfou'})
print(status)
```

### Options

- `consumer_key`: The consumer key
- `consumer_secret`: The consumer secret
- `oauth_token`: The OAuth token
- `oauth_token_secret`: The OAuth token secret
- `username`: The Fanfou username
- `password`: The Fanfou password
- `protocol`: Set the prototol, default is `http:`
- `api_domain`: Set the API domain, default is `api.fanfou.com`
- `oauth_omain`: Set the OAuth domain, default is `fanfou.com`
- `hooks`: Hooks allow modifications with OAuth

> For more Fanfou API docs, see the [Fanfou API doc](https://github.com/FanfouAPI/FanFouAPIDoc/wiki).

## API

```
ff.xauth()
ff.get(uri, params={})
ff.post(uri, params={}, files=None)
```

### Examples

```python
tl, _ = ff.get('/statuses/home_timeline')
print(tl)

st, _ = ff.post('/statuses/update', {status: 'hi flora'})
print(st)

st, _ = ff.post(
  '/photos/upload',
  params={'status': 'unicorn'},
  files={'photo': open('file_path', 'rb')}
)
print(st)
```

### Tips

Use `hooks` for your reverse-proxy server

```python
ff = Fanfou(
  consumer_key='',
  consumer_secret='',
  oauth_token='',
  oauth_token_secret='',
  api_domain='api.example.com',
  oauth_domain='example.com',
  hooks={
    'base_string': lambda s: s.replace('example.com', 'fanfou.com')
  }
)
```

## Related

- [fanfou-sdk-node](https://github.com/fanfoujs/fanfou-sdk-node) - Fanfou SDK for Node.js
- [fanfou-sdk-browser](https://github.com/fanfoujs/fanfou-sdk-browser) - Fanfou SDK for browser
- [fanfou-sdk-weapp](https://github.com/fanfoujs/fanfou-sdk-weapp) - Fanfou SDK for WeApp

## License

MIT
