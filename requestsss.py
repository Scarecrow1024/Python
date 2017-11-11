import requests
import json
from urllib import request
from bs4 import BeautifulSoup
import http.cookiejar
import ssl

try:
    headers = {
        'Host': 'github.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://github.com',
        'Connection': 'keep-alive',
    }
    ssl._create_default_https_context = ssl._create_unverified_context
    cj = http.cookiejar.CookieJar()
    opener = request.build_opener(request.HTTPCookieProcessor(cj))
    request.install_opener(opener)
    r1 = request.urlopen('https://github.com/login')
    soup = BeautifulSoup(r1.read().decode(), 'html.parser')
    token = soup.find("input", attrs={"name": "authenticity_token"})['value']
    print(token)
    formData = {
        'commit': 'Sign+in',
        'utf8': "✓",
        "login": '819681825@qq.com',
        "authenticity_token": token,
        "password": 'zyf941126',
    }

    r2 = requests.Session()
    print(r2)
    r = r2.post('https://github.com/session', data=json.dumps(formData), headers=headers)
    print(r.content)
except requests.exceptions.ConnectionError as e:
    print(e.strerror)
