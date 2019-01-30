# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderPageurlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()\

    url_page = scrapy.Field()#每一个详情页面的URL
    creat_time = scrapy.Field()  # 信息入库的时间
    flag = scrapy.Field()  # 爬取状态标志

