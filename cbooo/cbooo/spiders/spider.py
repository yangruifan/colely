# -*- coding: utf-8 -*-
import scrapy


class SpiderSpider(scrapy.Spider):
    name = 'spider'

    def start_requests(self):
        url = 'http://www.cbooo.cn/movies'


    def parse(self, response):
        pass
