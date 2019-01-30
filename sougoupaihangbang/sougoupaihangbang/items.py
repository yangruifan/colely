# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SougoupaihangbangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 电影名称
    name = scrapy.Field()
    # 第一层分类
    class_type_top1 = scrapy.Field()
    # 第二层分类
    class_type_top2 = scrapy.Field()
    # 搜狗搜索引擎指数
    sougou_number = scrapy.Field()
    # name md5加密
    name_hash = scrapy.Field()
    # 搜索引擎类型
    type = scrapy.Field()
    # 更新数据的时间
    create_time = scrapy.Field()
