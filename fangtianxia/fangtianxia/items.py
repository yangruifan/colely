# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeatherItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()、
    #分类
    name = scrapy.Field()
    num = scrapy.Field()
    # 指数值与详情
    zhishu = scrapy.Field()
    zhishu_details = scrapy.Field()
    # 市
    cityname = scrapy.Field()
    # 区
    areaname = scrapy.Field()
    areanum = scrapy.Field()
    # 省
    provincename = scrapy.Field()
    # 爬取时间
    fetch_time = scrapy.Field()
    # url
    url = scrapy.Field()
    source = scrapy.Field()
