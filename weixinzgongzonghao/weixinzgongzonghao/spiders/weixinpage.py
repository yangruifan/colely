# -*- coding: utf-8 -*-
import scrapy


class WeixinpageSpider(scrapy.Spider):
    name = 'weixinpage'
    allowed_domains = ['www']
    start_urls = ['http://www/']

    def parse(self, response):
        pass
