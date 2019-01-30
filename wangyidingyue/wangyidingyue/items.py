# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YellowurlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    # Spider_company

    # 地址
    url = scrapy.Field()
    # 地址哈希
    url_hash = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 内容
    content = scrapy.Field()
    # 发布时间
    creat_time = scrapy.Field()
    # 爬取时间
    fetch_time = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 分类
    topic = scrapy.Field()
    # 点赞数
    like_num = scrapy.Field()
    #是否有照片
    has_img = scrapy.Field()




