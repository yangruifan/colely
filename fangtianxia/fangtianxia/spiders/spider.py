# -*- coding: utf-8 -*-
import scrapy
from urllib import parse

class SpiderSpider(scrapy.Spider):
    name = 'spider'

    def start_requests(self):
        url = 'https://esf.fang.com/newsecond/esfcities.aspx'
        yield scrapy.Request(url=url,
                             dont_filter=True,
                             )

    def parse(self, response):
        urllist = response.css("div.onCont ul li a::attr(href)").extract()
        urllist = list(set(urllist))
        urls = []
        for url in urllist:
            urls.append(parse.urljoin(url, '/housing/'))
        for url in urls:
            yield scrapy.Request(url=url,
                                 dont_filter=True,
                                 callback=self.get_first,
                                 )

    def get_first(self, response):
        if response.status == 200:
            next_url = ''
            try:
                next_url = response.css("#PageControl1_hlk_next::attr(href)").first_extract()
                next_url = parse.urljoin(response.url, next_url)
            except:
                pass
        else:
            pass


