# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
try:
    import  urlparse as parse
except:
    from urllib import parse

class MaoyanspiderSpider(scrapy.Spider):
    name = 'maoyanspider'
    allowed_domains = ['www']
    start_urls = ['http://maoyan.com/query?kw=']
    movie = "一出好戏"
    def start_requests(self):
        url = 'http://maoyan.com/query?kw={0}'.format(self.movie)
        yield Request(url= url)
    def parse(self, response):
        url_son = response.css("dl.movie-list dd div a::attr(href)").extract_first()
        url = parse.urljoin(response.url, url_son)
        yield Request(url= url,callback= self.one_page,dont_filter= True)

    def one_page(self,response):
        print(response.text)
        pass
