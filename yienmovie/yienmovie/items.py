# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YienmovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Companyname = scrapy.Field()  # 公司名称
    CompanyID = scrapy.Field()  # 公司ID
    CinemaID = scrapy.Field()  # 影院id
    CinemaName = scrapy.Field()  # 影院名称
    Province = scrapy.Field()  # 省份
    City = scrapy.Field()  # 城市
    Area = scrapy.Field()  # 地区
    OnlineDate = scrapy.Field()  # 开业时间
    Screen = scrapy.Field()  # 银幕数
    ScreenD = scrapy.Field()  # 3D银幕
    ScreenS = scrapy.Field()  # 数字
    Seat = scrapy.Field()  # 座位
    Tel = scrapy.Field()  # 电话
    Creat_time = scrapy.Field()
    source = scrapy.Field()
    sqltype = scrapy.Field()

class PeerItem(scrapy.Item):
    Companyname = scrapy.Field()  # 公司名称
    CompanyID = scrapy.Field()  # 公司ID
    CompanyId = scrapy.Field()  # 合作公司ID
    CompanyName = scrapy.Field()  # 合作公司名称
    Num = scrapy.Field()  # 合作数
    CompanyType = scrapy.Field()  # 合作类型
    Creat_time = scrapy.Field()  # 爬取时间
    source = scrapy.Field()  # 来源
    sqltype = scrapy.Field()