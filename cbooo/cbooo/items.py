# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PeerItem(scrapy.Item):
    movie = scrapy.Field()  # 电影名称
    movie_hash = scrapy.Field()  # 电影名称hash
    creat_time = scrapy.Field()  # 文章创建时间
    source = scrapy.Field()  # 来源
    event = scrapy.Field()  # 事件类型
    title = scrapy.Field()  # 文章标题
    page_source = scrapy.Field()  # 文章来源
    url = scrapy.Field()  # 文章url
    url_hash = scrapy.Field()  # 文章url
    fetch_time = scrapy.Field()  # 爬取的时间