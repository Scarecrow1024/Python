# -*- coding: utf-8 -*-
from scrapy import Request, Spider
from ..items import QkItem


class QkscSpider(Spider):
    name = 'qksc'
    allowed_domains = ['588ku.com']
    start_urls = ['http://588ku.com/']

    start_page =901
    url_init = 'http://588ku.com/sucai/0-dnum-0-45-0-{page}/'


    def start_requests(self):
        yield Request(self.url_init.format(page=self.start_page), self.parse_sc, meta={'proxy':'http://127.0.0.1:38252'})

    def parse_sc(self, response):
        for item in response.xpath('//*[@id="element"]/div/div[1]'):
            link = item.xpath('.//a[1]/@href').extract_first()
            yield Request(link, self.parse_link, meta={'proxy':'http://127.0.0.1:38252'})

    def parse_link(self, response):
        url = response.url
        fav = response.xpath('//*[@id="collect-btn"]/b/text()').extract_first()
        view = response.xpath('/html/body/div[2]/div[3]/div[2]/div[1]/div/span[1]/b/text()').extract_first()
        down = response.xpath('/html/body/div[2]/div[3]/div[2]/div[1]/div/span[2]/b/text()').extract_first()
        img = response.xpath('/html/body/div[2]/div[3]/div[1]/div/img/@src').extract_first()
        title = response.xpath('/html/body/div[2]/div[3]/div[1]/div/img/@title').extract_first()
        recom = ''
        for item in response.xpath('/html/body/div[2]/div[3]/div[3]/div[1]/a'):
            recom += item.xpath('.//text()').extract_first() + ':' + item.xpath('.//@href').extract_first() + '\\'

        attr = ''
        for item in response.xpath('/html/body/div[2]/div[3]/div[2]/ul/li'):
            attr += item.xpath('.//*').extract_first() + '/'

        item = QkItem()
        item['title'] = title
        item['url'] = url
        item['img'] = img
        item['view'] = view
        item['down'] = down
        item['fav'] = fav
        item['recom'] = recom
        item['attr'] = attr
        item['kind'] = '45'

        yield item
        for page in range(902,1000):
            yield Request(self.url_init.format(page=page), self.parse_sc, meta={'proxy':'http://127.0.0.1:38252'})


