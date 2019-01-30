# -*- coding: utf-8 -*-
import scrapy


class FashionSpiderSpider(scrapy.Spider):
    name = 'fashion_spider'
    allowed_domains = ['www.bashalady.com']
    start_urls = ['http://www.bashalady.com/']

    def parse(self, response):
        pass
