# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class ZhihuItem(Item):
    name = Field()
    answer_count = Field()
    articles_count = Field()
    headline = Field()
    url_token = Field()
    gender = Field()
