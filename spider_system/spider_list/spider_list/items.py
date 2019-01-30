# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderListItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    source_id = scrapy.Field()
    flag = scrapy.Field()


class SpiderPageurlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()\

    url = scrapy.Field()#每一个详情页面的URL
    creat_time = scrapy.Field()  # 信息入库的时间
    flag = scrapy.Field()  # 爬取状态标志
    source_id = scrapy.Field()#

class SpiderPageItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()#目标
    author = scrapy.Field()#作者
    content = scrapy.Field()#内容
    creat_time = scrapy.Field()#创建时间
    fetch_time = scrapy.Field()#爬取时间
    status = scrapy.Field()#标志
    read_num = scrapy.Field()#阅读数量
    like_num = scrapy.Field()#点赞数
    source = scrapy.Field()#来源
    url = scrapy.Field()#文章得url
    source_id = scrapy.Field()
