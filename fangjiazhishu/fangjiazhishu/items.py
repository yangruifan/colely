# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FangjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()、
    #分类
    cityname = scrapy.Field()
    cityname_hash = scrapy.Field()
    # 指数值与详情
    fetch_time = scrapy.Field()
    creat_time = scrapy.Field()
    num = scrapy.Field()
    url = scrapy.Field()
    # 市scrapy.Field()
    source = scrapy.Field()


