# -*- coding: utf-8 -*-
import scrapy


class StarpaihangSpider(scrapy.Spider):
    name = 'starpaihang'
    # start_urls = ['http://www.xunyee.cn/']

    def start_requests(self):
        urls = ['http://www.xunyee.cn/rank-person-index-0.html',
                'http://www.xunyee.cn/rank-person-index-1.html',
                'http://www.xunyee.cn/rank-person-index-2.html',
                'http://www.xunyee.cn/rank-person-index-3.html']
        for url in urls:
            yield scrapy.Request(url=url, dont_filter=True)

    def parse(self, response):
        if 'index-0' in response.url:
            print(111)
        if 'index-1' in response.url:
            print(112)
        if 'index-2' in response.url:
            print(113)
        if 'index-3' in response.url:
            print(114)
        pass
