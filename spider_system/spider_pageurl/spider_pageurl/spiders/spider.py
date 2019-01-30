# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import re

try:
    import urlparse as parse
except:
    from urllib import parse
from spider_pageurl.items import SpiderPageurlItem
import time

class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['example.com']
    start_urls = ['']

    def start_requests(self):
        while 1:
            url = "http://www.duwenzhang.com/wenzhang/gaoxiaowenzhang/"#http://www.duwenzhang.com/wenzhang/gaoxiaowenzhang/
            flag = ""
            list_rule = "//td[@valign='top']/table"#//div[@class='contentholder']/div
            yield Request(url=url, meta={"list_rule": list_rule}, dont_filter=True)

    def parse(self, response):
        urlitem = SpiderPageurlItem()
        all_list = response.xpath(response.meta["list_rule"]).extract()
        for one in all_list:
            reg = '.*?<a href="(.*?)"( |>).*?'
            url = re.search(reg, one, re.S).group(1)
            url = parse.urljoin(response.url, url)
            print(url)
            urlitem["url_page"] = url
            urlitem["creat_time"] = time.strftime("%Y-%m-%d", time.localtime())
            urlitem["flag"] = 0
            # yield urlitem
