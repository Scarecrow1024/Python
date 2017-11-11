# -*- coding: utf-8 -*-
from scrapy import Request, Spider, FormRequest
from ..items import MiyuansuItem


class MikwSpider(Spider):
    name = 'mikw'
    allowed_domains = ['51yuansu.com']
    start_urls = ['http://51yuansu.com/']
    meta = {'proxy': 'http://127.0.0.1:38249'}
    search_url = 'http://www.51yuansu.com/index.php?m=Index&a=pinYin&k={key_word}'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    def start_requests(self):
        keyword = '双十一'
        return Request(self.search_url.format(key_word=keyword), headers=self.headers, meta=self.meta)

    def parse(self, response):
        pass
