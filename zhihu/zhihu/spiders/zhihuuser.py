# -*- coding: utf-8 -*-
import json

from scrapy import Spider, Request

from ..items import ZhihuItem


class ZhihuuserSpider(Spider):
    name = 'zhihuuser'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    start_user = 'excited-vczh'

    follows_query = 'data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'
    follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    user_query = 'allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    followers_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
    followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'

    def start_requests(self):
        yield Request(self.follows_url.format(include=self.follows_query, user=self.start_user, offset=0, limit=20), callback=self.parse_follows)
        yield Request(self.followers_url.format(include=self.followers_query, user=self.start_user, offset=0, limit=20),
                      callback=self.parse_followers)
        yield Request(self.user_url.format(include=self.user_query, user=self.start_user), callback=self.parse_user)

    def parse_follows(self, response):
        results = json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(include=self.user_query, user=result.get('url_token')), callback=self.parse_user)
        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next = results.get('paging').get('next')
            yield Request(next, callback=self.parse_follows)

    def parse_followers(self, response):
        results = json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(include=self.user_query, user=result.get('url_token')), callback=self.parse_user)
        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next = results.get('paging').get('next')
            yield Request(next, callback=self.parse_follows)

    def parse_user(self, response):
        result = json.loads(response.text)
        item = ZhihuItem()
        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)
        yield item
        yield Request(self.follows_url.format(include=self.follows_query, user=result.get('url_token'), offset=0, limit=20), callback=self.parse_follows)
        yield Request(self.followers_url.format(include=self.followers_query, user=result.get('url_token'), offset=0, limit=20), callback=self.parse_followers)
