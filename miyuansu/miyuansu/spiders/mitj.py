# -*- coding: utf-8 -*-
from scrapy import Request, Spider
from ..items import MiyuansuItem
import pymongo

class MiysSpider(Spider):
    collection_name = 'miys'
    mongo_uri = 'localhost'
    mongo_db = 'miys'
    client = pymongo.MongoClient(mongo_uri)

    # def close_spider(self, spider):
    #     pymongo.MongoClient(self.mongo_uri).close()

    # def process_item(self, item, spider):
    #     self.db[self.collection_name].update({'bianhao':item['bianhao']}, {'$set':item}, True)
    meta = {'proxy': 'http://127.0.0.1:38252'}
    name = 'mitj'
    allowed_domains = ['www.51yuansu.com']
    start_urls = ['http://www.51yuansu.com/']

    start_page = 1
    start_cat_1 = 2
    start_cat_2 = 37


    count = 0
    collection_init = client[mongo_db][collection_name].find_one({'is_spider':'0'})

    def start_requests(self):
        #每次获取第一条没有爬取过的详情页链接

        #获取之后将该collection更新为已抓取
        #student['age'] = 26
        is_spider = self.collection_init
        is_spider['is_spider'] = '1'
        self.client[self.mongo_db][self.collection_name].update_one({'bianhao':is_spider['bianhao']}, {'$set': is_spider})
        self.client.close()
        print('+++++++++++++++++')
        print(is_spider['url'])
        print('+++++++++++++++++')
        yield Request(is_spider['url'], self.parse_sc, meta=self.meta, dont_filter = True)

    def parse_next(self, response):
        self.count = 0
        for item in response.xpath('//*[@id="f-content"]/div/div[1]'):
            self.count = self.count+1
            link = item.xpath('.//a/@href').extract_first()
            print('======================')
            print(self.count, link)
            print('======================')
            yield Request(link, self.parse_link, meta=self.meta, dont_filter = True)
            if self.count == 8:
                self.count = 0
                print('++++++++++++++++++')
                next_collect = pymongo.MongoClient(self.mongo_uri)[self.mongo_db][self.collection_name].find_one({'is_spider': '0'})
                next_url = next_collect['url']
                next_collect['is_spider'] = 1
                self.client[self.mongo_db][self.collection_name].update_one({'bianhao': next_collect['bianhao']},{'$set': next_collect})
                print(next_url)
                print('++++++++++++++++++')
                # yield Request(next_url, self.start_requests, meta=self.meta)
                yield Request(next_url, self.parse_next, meta=self.meta, dont_filter=True)


    def parse_sc(self, response):
        for item in response.xpath('//*[@id="f-content"]/div/div[1]'):
            link = item.xpath('.//a/@href').extract_first()
            yield Request(link, self.parse_link, meta=self.meta, dont_filter = True)

    def parse_link(self, response):
        url = response.url

        cat_1_link = response.xpath('/html/body/div[3]/div/div[1]/h3/a[2]/@href').extract_first()
        cat_2_link = response.xpath('/html/body/div[3]/div/div[1]/h3/a[3]/@href').extract_first()
        cat_1_data = cat_1_link.split('=')
        cat_1 = cat_1_data[-1:][0]
        cat_2_data = cat_2_link.split('=')
        cat_2 = cat_2_data[-1:][0]
        print('**************')
        print(cat_1[0], cat_2[0])
        print('**************')
        #cat_1 = self.start_cat_1
        #cat_2 = self.start_cat_2
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
        item['is_spider'] = '0'
        self.count = self.count + 1
        if self.count == 8:
            print('++++++++++++++++++')
            next_collect = pymongo.MongoClient(self.mongo_uri)[self.mongo_db][self.collection_name].find_one({'is_spider': '0'})
            next_collect['is_spider'] = 1
            self.client[self.mongo_db][self.collection_name].update_one({'bianhao': next_collect['bianhao']},{'$set': next_collect})
            next_url = next_collect['url']
            print(next_url)
            print('++++++++++++++++++')
            #yield Request(next_url, self.start_requests, meta=self.meta)
            yield Request(next_url, self.parse_next, meta=self.meta, dont_filter = True)
        yield item

        # i = 1
        # while True:
        #     next_url = self.client.find_one({'is_spider': '0'})['url']
        #     print(next_url)
        #     i = i + 1
        #     print(i)
        #     #yield Request(next_url, self.parse_sc, meta = self.meta)


