from asgiref.sync import sync_to_async
import requests
import asyncio
import json


@sync_to_async()
def get_curs():
    value = ['USD', 'AED', 'EUR']
    payload = {}
    headers = {
        "apikey": "L2sk6D6aFkKZSo30HUjNTs49F6ktYrz8"
    }
    res = {}
    for v in value:
        url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={v}"
        result = requests.request("GET", url, headers=headers, data=payload)

        result = json.loads(result.text)
        res[f'{v}RUB'] = result['rates']['RUB']
        res['timestamp'] = result['timestamp']
    print(res)


