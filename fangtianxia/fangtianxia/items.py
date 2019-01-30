# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FangtianxiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    city = scrapy.Field()
    url = scrapy.Field()
    url_hash = scrapy.Field()
    oldprice = scrapy.Field()
    nowprice = scrapy.Field()
    xiaoqudizhi = scrapy.Field()
    lvhualv = scrapy.Field()
    wuyegongsi = scrapy.Field()
    jianzhujiegou = scrapy.Field()
    rongjilv = scrapy.Field()
    youbian = scrapy.Field()
    loudong = scrapy.Field()
    wuyefei = scrapy.Field()
    jianzhuniandai = scrapy.Field()
    kaifashang = scrapy.Field()
    jianzhumianji = scrapy.Field()
    fangwuzongshu = scrapy.Field()
    wuyeleibie = scrapy.Field()
    fujiaxinxi = scrapy.Field()
    zhandimianji = scrapy.Field()
    jianzhuleixing = scrapy.Field()
    chanquanmiansu = scrapy.Field()
    suoshuquyu = scrapy.Field()
