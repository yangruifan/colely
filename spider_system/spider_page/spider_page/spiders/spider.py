# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import re
try:
    import  urlparse as parse
except:
    from urllib import parse
from spider_page.items import SpiderPageItem

class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['example.com']
    start_urls = ['']
    def start_requests(self):
        """
        flag 标志位：是否已经爬取
        title 标题：文章标题
        content 内容：文章的内容
        author 作者：文章的作者
        creat_time 时间：文章发表的时间
        :return:
        """
        while 1:

            url = "http://www.milk.com.hk/content/%E5%88%A5%E6%B3%A8%E5%A8%81%E5%A3%AB%E5%BF%8C-johnnie-walker-x-hbo%E6%AC%8A%E5%8A%9B%E9%81%8A%E6%88%B2-white-walker-johnnie-walker"
            flag = ""
            title = "//h2[@class='headtitle']/text()"
            content = "//div[@class='node']"
            author = ""
            creat_time = "//td[@valign='top']/span/text()"
            source = ""
            yield Request(url=url,
                          meta={
                              "title":title,
                              "content":content,
                              "author":author,
                              "creat_time":creat_time,
                              "source":source,
                          },
                          dont_filter=True)

    def parse(self, response):
        """
        flag 标志位：是否已经爬取
        title 标题：文章标题
        content 内容：文章的内容
        author 作者：文章的作者
        creat_time 时间：文章发表的时间
        :return:
        """
        pageitem = SpiderPageItem()

        title = response.xpath(response.meta["title"])
        # author = response.xpath(response.meta["author"])
        content = response.xpath(response.meta["content"])
        creat_time = response.xpath(response.meta["creat_time"])
        # source = response.xpath(response.meta["source"])

        pageitem["url"] = response.url
        pageitem["title"] = title
        # pageitem["author"] = author
        pageitem["content"] = content
        pageitem["creat_time"] = creat_time
        # pageitem["source"] = source

        pass
