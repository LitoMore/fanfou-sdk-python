from fanfou_sdk import Fanfou

ff = Fanfou(
    consumer_key='13456aa784cdf7688af69e85d482e011',
    consumer_secret='f75c02df373232732b69354ecfbcabea'
)

text, r = ff.request_token()

print(text, r.status_code)
