# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SougouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 电影名称
    name = scrapy.Field()
    # 第一层分类
    name_hash = scrapy.Field()
    # 第二层分类
    allavg = scrapy.Field()
    # 搜狗搜索引擎指数
    wiseavg = scrapy.Field()
    # 搜索引擎类型
    source = scrapy.Field()
    # 更新数据的时间
    create_time = scrapy.Field()
    fetch_time = scrapy.Field()
    #
    sql_flag = scrapy.Field()
    flag = scrapy.Field()
