# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class QkItem(Item):
    title = Field()
    url = Field()
    img = Field()
    view = Field()
    down = Field()
    fav = Field()
    recom = Field()
    attr = Field()
    kind = Field()
