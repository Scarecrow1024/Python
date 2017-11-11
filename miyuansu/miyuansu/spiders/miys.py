# -*- coding: utf-8 -*-
from scrapy import Request, Spider
from ..items import MiyuansuItem

#scrapy crawl somespider -s JOBDIR=crawls/somespider-1
class MiysSpider(Spider):
    name = 'miys'
    allowed_domains = ['www.51yuansu.com']
    start_urls = ['http://www.51yuansu.com/']
    #meta = {'proxy': 'http://127.0.0.1:38252'}
    meta = {}

    start_page = 1
    start_cat_1 = 5
    start_cat_2 = 29
    url_init = 'http://www.51yuansu.com/index.php?m=Index&a=fenlei&st=2&bc={cat_1}&c={cat_2}&p={page}'

    def start_requests(self):
        yield Request(self.url_init.format(cat_1=self.start_cat_1, cat_2=self.start_cat_2, page=self.start_page, meta=self.meta), self.parse_sc)

    def parse_sc(self, response):
        for item in response.xpath('//*[@id="f-content"]/div/div[1]'):
            link = item.xpath('.//a/@href').extract_first()
            yield Request(link, self.parse_link, meta=self.meta)

    def parse_link(self, response):
        url = response.url
        cat_1 = self.start_cat_1
        cat_2 = self.start_cat_2
        #cat_1_link = response.xpath('/html/body/div[3]/div/div[1]/h3/a[2]/@href').extract_first()
        #cat_2_link = response.xpath('/html/body/div[3]/div/div[1]/h3/a[3]/@href').extract_first()
        #cat_1_data = cat_1_link.split('=')
        #cat_1 = cat_1_data[-1:][0]
        #cat_2_data = cat_2_link.split('=')
        #cat_2 = cat_2_data[-1:][0]
        fav = response.xpath('/html/body/div[3]/div/div[2]/div[2]/div[2]/div[2]/span[3]/text()').extract_first()
        view = response.xpath('/html/body/div[3]/div/div[2]/div[2]/div[2]/div[2]/span[1]/text()').extract_first()
        down = response.xpath('/html/body/div[3]/div/div[2]/div[2]/div[2]/div[2]/span[2]/text()').extract_first()
        img = response.xpath('/html/body/div[3]/div/div[2]/div[1]/div[2]/img/@src').extract_first()
        title = response.xpath('/html/body/div[3]/div/div[2]/div[1]/div[1]/h3/text()').extract_first()
        bianhao = response.xpath('/html/body/div[3]/div/div[2]/div[2]/div[3]/p[1]/text()').extract_first()
        size = response.xpath('/html/body/div[3]/div/div[2]/div[2]/div[3]/p[3]/text()').extract_first()
        format = response.xpath('/html/body/div[3]/div/div[2]/div[2]/div[3]/p[2]/text()').extract_first()
        dpi = response.xpath('/html/body/div[3]/div/div[2]/div[2]/div[3]/p[4]/text()').extract_first()
        time = response.xpath('/html/body/div[3]/div/div[2]/div[2]/div[3]/p[5]/text()').extract_first()
        desc = response.xpath('/html/body/div[3]/div/div[2]/div[1]/div[3]/p/text()').extract_first()


        item = MiyuansuItem()
        item['title'] = title
        item['url'] = url
        item['cat_1'] = cat_1
        item['cat_2'] = cat_2
        item['dpi'] = dpi
        item['img'] = img
        item['view'] = view
        item['down'] = down
        item['fav'] = fav
        item['bianhao'] = bianhao
        item['size'] = size
        item['format'] = format
        item['time'] = time
        item['desc'] = desc
        item['is_spider'] = 0

        yield item
        for page in range(2,334):
            yield Request(self.url_init.format(cat_1=self.start_cat_1, cat_2=self.start_cat_2, page=page), self.parse_sc, meta=self.meta)


