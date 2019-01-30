# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PageItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()、
    #分类
    url = scrapy.Field()
    url_hash = scrapy.Field()
    title = scrapy.Field()
    has_img = scrapy.Field()
    content = scrapy.Field()
    creat_time = scrapy.Field()
    fetch_time = scrapy.Field()
    source = scrapy.Field()
