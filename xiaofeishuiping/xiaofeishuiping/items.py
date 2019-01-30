# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XiaofeiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()、
    # 分类
    name = scrapy.Field()
    # 发布的时间
    creat_time = scrapy.Field()
    # 指数值与详情
    name_code = scrapy.Field()
    # 指数
    indexs = scrapy.Field()
    # 爬取时间
    fetch_time = scrapy.Field()
    # 地区
    city = scrapy.Field()
    city_code = scrapy.Field()
    # 来源
    source = scrapy.Field()
