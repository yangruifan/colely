# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import re
try:
    import  urlparse as parse
except:
    from urllib import parse
from spider_list.items import SpiderPageItem
from spider_list.Operate_datebase_table import Operate_datebase_table
import time

class SpiderSpider(scrapy.Spider):
    name = 'spider_page'
    def start_requests(self):
        """
        flag 标志位：是否已经爬取
        title 标题：文章标题
        content 内容：文章的内容
        author 作者：文章的作者
        creat_time 时间：文章发表的时间
        :return:
        """
        connect = Operate_datebase_table("adv_spider_article_link")  # 链接文章列表
        # data = connect.selectTable("url","fetched=0")
        url = connect.selectTable("(url,source_id,id)", "fetched=0")#查找文章列表是否有待爬url
        if url != ():#(('你好，之华',), ('触不可及',), ('李茶的姑妈',))
            for url_one in url:#('你好，之华',)
                data_connect = Operate_datebase_table("adv_spider_source")#链接规则列表
                #根据 源id 查找标题、内容的匹配规则
                datas = data_connect.selectTable("(extract_tittle_rule,extract_content_rule)", "id={0}".format(url_one[1]))
                #((‘标题规则’，‘内容规则’))
                title = datas[0][0]
                content = datas[0][1]
                source_id = url_one[2]
                yield Request(url=url_one[0],
                              meta={
                                  "title": title,
                                  "content": content,
                                  "source_id": source_id,
                              },
                              dont_filter=True,
                              priority=1)

        else:
            return 0

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

        title = response.xpath(response.meta["title"]).extract_first()
        # author = response.xpath(response.meta["author"])
        content = response.xpath(response.meta["content"]).extract_first()
        # creat_time = response.xpath(response.meta["creat_time"])
        # source = response.xpath(response.meta["source"])

        pageitem["url"] = response.url
        pageitem["title"] = title
        pageitem["source_id"] = response.meta["source_id"]
        # pageitem["author"] = author
        pageitem["content"] = content
        # pageitem["creat_time"] = creat_time
        # pageitem["source"] = source
        yield pageitem

        updata_connect = Operate_datebase_table("adv_spider_article_link")  # 链接文章列表
        updata_connect.updateTale({'fetched': '1', }, 'url="{}"'.format(response.url))  # 更改列表url待爬标志位

