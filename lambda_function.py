import requests


def lambda_handler(event, context):
    res = requests.get('http://httpbin.org/ip')
    return res.json()
