import gevent, time, pymysql
import hashlib
import requests
import os
from gevent import monkey

monkey.patch_all()


def down_img(url):
    proxies = {
        "http": '127.0.0.1:38251',
    }
    res = requests.get(url, proxies=proxies)
    print(res.text)

if __name__ == "__main__":
    while True:
        time.sleep(1)
        down_img('http://local.png666.com/api/down/down')
