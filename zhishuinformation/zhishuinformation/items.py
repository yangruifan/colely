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

    # 电影名称
    name = scrapy.Field()
    #name 哈希
    name_hash = scrapy.Field()
    # 当天指数总数
    allavg = scrapy.Field()
    # PC端指数总数
    pcavg = scrapy.Field()
    # 移动端指数总数
    wiseavg = scrapy.Field()
    # 资讯类指数总数
    avg = scrapy.Field()
    # 国家地区指数分布情况
    countrydata = scrapy.Field()
    # 广东省指数分布情况
    citydata = scrapy.Field()
    # 日期
    date = scrapy.Field()
    # 时间戳
    flag = scrapy.Field()
    # sql语句类型判断
    sql_flag = scrapy.Field()
    # 来源
    source = scrapy.Field()
    creat_time = scrapy.Field()


class YellItem(scrapy.Item):
    # 电影名称
    name = scrapy.Field()
    # name 哈希
    name_hash = scrapy.Field()
    # 时间戳
    flag = scrapy.Field()
    # sql语句类型判断
    sql_flag = scrapy.Field()
    # 日期
    date = scrapy.Field()
    # 年龄段
    before_nineteen = scrapy.Field()
    twenty_to_thirty = scrapy.Field()
    thirty_to_forty = scrapy.Field()
    forty_to_fifty = scrapy.Field()
    aften_fifty = scrapy.Field()
    # 性别分布
    men = scrapy.Field()
    women = scrapy.Field()
    # 来源
    source = scrapy.Field()


class YeItem(scrapy.Item):
    # 电影名称
    name = scrapy.Field()
    # name 哈希
    name_hash = scrapy.Field()
    # sql语句类型判断
    sql_flag = scrapy.Field()
    # 日期
    date = scrapy.Field()
    # 爬取的时间
    run_time = scrapy.Field()
    # 相关字名
    link_name = scrapy.Field()
    # one
    No0 = scrapy.Field()
    # two
    No1 = scrapy.Field()
    # three
    No2 = scrapy.Field()
    # four
    No3 = scrapy.Field()
    # five
    No4 = scrapy.Field()
    # 时间戳
    flag = scrapy.Field()
    # sql语句类型判断
    sql_flag = scrapy.Field()
    # 来源
    source = scrapy.Field()

class Diquitem(scrapy.Item):
    # 查询指数的时间段
    date = scrapy.Field()
    # 地区
    region = scrapy.Field()
    # 地区代号
    regionnum = scrapy.Field()
    # 爬取的时间
    fetch_time = scrapy.Field()
    # 指数
    indexs = scrapy.Field()
    # 电影
    movie = scrapy.Field()
    movie_hash = scrapy.Field()
    # 标志相对的排行耪
    billboard = scrapy.Field()
    # 来源
    source = scrapy.Field()
    # sql语句类型判断
    sql_flag = scrapy.Field()