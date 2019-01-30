# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaijiahaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()、
    #关键字
    name = scrapy.Field()
    # 标题
    tittle = scrapy.Field()
    tittle_hash = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 作者简介
    author_desc = scrapy.Field()
    # 来源
    source = scrapy.Field()
    # 创建时间
    create_time = scrapy.Field()
    # 爬取的时间
    spider_time = scrapy.Field()
    # 内容
    content = scrapy.Field()
    # 文章url
    url = scrapy.Field()

    pass