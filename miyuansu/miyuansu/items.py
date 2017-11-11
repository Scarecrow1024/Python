# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class MiyuansuItem(Item):
    title = Field()
    url = Field()
    img = Field()
    view = Field()
    down = Field()
    fav = Field()
    cat_1 = Field()
    cat_2 = Field()
    size = Field()
    bianhao = Field()
    format = Field()
    time = Field()
    desc = Field()
    dpi = Field()
    is_spider = Field()
