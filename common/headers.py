# common/headers.py
from common.config import TOKEN


def get_headers():
    return {

        "Accept": "*/*",

        "Content-Type": "application/json",

        "Accept-Language": "zh-CN,zh;q=0.9",

        "Origin": "https://www-h5.flextv9.com",

        "User-Agent": "Mozilla/5.0",

        "apiUrl": "cbaa27d88358941040262d26df29403f",

        "appId": "859mw3lnt40rxbca",

        "deviceNumber": "fbc7db85-7c63-4467-a458-e7aaf7a5366d",

        "gmtTd": "8",

        "lang": "en",

        "signature": "b8d5c9e21526f6337c6ae0aa9db8c2e93f8286c7216b22bf5339bd732d9318ef",

        "timeZone": "Asia/Shanghai",

        "timestamp": "1785835751",

        "token": TOKEN

    }
