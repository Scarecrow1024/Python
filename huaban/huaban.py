# -*- coding: utf-8 -*-
import requests
import time
import json
import re
import os
from urllib import request
from pyquery import PyQuery as PQ
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import threading
import gevent
from gevent import monkey

monkey.patch_all()

class Huaban(object):
    def __init__(self):
        self.username = '15639128975'
        self.password = 'zyf941024'
        self.pages = 20
        self.array = []
        self.results = []
        self.proxies = {"http": "http://127.0.0.1:8087"}

    def login(self):
        data = {
            'email': self.username,
            'password': self.password,
            '_ref': 'frame'
        }
        s = requests.Session()
        s.post('https://huaban.com/auth/', data=data, verify=False)
        # r = s.get('http://huaban.com/drbitiom09/', verify=False)
        # return r.content
        return s

    def get_first_url(self):  # 获取第一页的链接
        #s = self.login()
        #r = requests.get('http://huaban.com/boards/36918436/')
        r = requests.get('http://huaban.com/boards/30425412/')
        raw = r.content.decode('utf-8')
        prog = re.compile(r'app\.page\["board"\].*')
        appPins = prog.findall(raw)
        m = re.match(r'app\.page\["board"\] = (.*?)', appPins[0])
        # return m.string
        m = m.string.replace(';', '')
        loads = m.replace('app.page["board"] = ', '')
        for item in json.loads(loads)['pins']:
            self.array.append(item['pin_id'])
        return 'http://huaban.com/boards/36918436/?j4viuily&max='+str(self.array[29])+'&limit=20&wfl=1'

    def get_urls(self):  # 获取接下来采集页的链接
        url = self.get_first_url()
        page = self.pages
        while page > 0:
            r = requests.get(url)
            raw = r.content.decode('utf-8')
            prog = re.compile(r'app\.page\["board"\].*')
            appPins = prog.findall(raw)
            m = re.match(r'app\.page\["board"\] = (.*?)', appPins[0])
            # return m.string
            m = m.string.replace(';', '')
            loads = m.replace('app.page["board"] = ', '')
            for item in json.loads(loads)['pins']:
                self.array.append(item['pin_id'])
            url = 'http://huaban.com/boards/36918436/?j4viuily&max='+str(self.array[-1:][0])+'&limit=20&wfl=1'
            #print(url)
            page -= 1
        return self.array

    def get_img_url(self):
        self.get_urls()
        for pins in self.array:
            url = 'http://huaban.com/pins/'+str(pins)+'/'
            r = requests.get(url)
            #p = PQ.text(r.text)
            raw = r.content.decode('utf-8')
            prog = re.compile(r'app\.page\["pin"\].*')
            appPins = prog.findall(raw)
            m = re.match(r'app\.page\["pin"\] = (.*?)', appPins[0])
            # return m.string
            m = m.string.replace(';', '')
            loads = m.replace('app.page["pin"] = ', '')
            res = json.loads(loads)
            self.results.append(res['file']['key'])
            print(self.down_img(res['file']['key']))
        return self.results

    def down_img(self, pin_id):
        link = 'http://img.hb.aicdn.com/'+str(pin_id)
        #proxy_support = request.ProxyHandler({'http': '127.0.0.1:8087'})
        #opener = request.build_opener(proxy_support)
        #request.install_opener(opener)
        r = request.urlopen(link)
        img = r.read()
        img_name = os.path.join("C:\Python\huaban\iards", pin_id+'.jpg')
        with open(img_name, 'wb') as pic:
            pic.write(img)
        return link

if __name__ == "__main__":
    start1 = time.time()
    huaban = Huaban()
    data = huaban.get_img_url()

    l = []
    for i in data:
        l.append(gevent.spawn(huaban.down_img, i))
    gevent.joinall(l)

    """
    for i in data:
        p = threading.Thread(target=huaban.down_img(), args=("%s" % i,))
        p.start()
    p.join()
    start2 = time.time()
    print(start2 - start1)
    """
