# -*- coding: utf-8 -*-
import scrapy
import json
import re
from spider_list.Operate_datebase_table import Operate_datebase_table
try:
    import urlparse as parse
except:
    from urllib import parse
from spider_list.items import SpiderPageurlItem
import time

class SpiderSpider(scrapy.Spider):
    name = 'spider_pageurl'

    def start_requests(self):
        connect = Operate_datebase_table("adv_spider_list_link")  # 链接文章列表
        #while 1:
        try:
            url = connect.selectTable("(url,source_id)", "fetched=0")  # 查找列表url是否有待爬
        except:
            print("查询列表url错误！")
        if url != ():#(('你好，之华',), ('触不可及',), ('李茶的姑妈',))
            for url_one in url:  # ('你好，之华',)
                data_connect = Operate_datebase_table("adv_spider_source")  # 链接规则列表
                # 根据 源id 查找标题、内容的匹配规则
                datas = data_connect.selectTable("(extract_list_rule)",
                                                     "id={0}".format(url_one[1]))
                list_rule = datas[0][0]
                print(url_one[0])
                yield scrapy.Request(url=url_one[0],
                                     meta={
                                         "list_rule": list_rule,
                                         "source_id":url_one[1],
                                     },
                                     callback=self.parse,
                                     dont_filter=True,
                                     priority=1)
                updata_connect = Operate_datebase_table("adv_spider_list_link")  # 链接文章列表
                updata_connect.updateTale({'fetched': '1', }, 'url="{}"'.format(url_one[0]))  # 查找列表url是否有待爬


        else:
            return 0

    def parse(self, response):
        urlitem = SpiderPageurlItem()
        if 'xpath:' in response.meta["list_rule"]:
            all_list = response.xpath(response.meta["list_rule"][6:]).extract()
            for url in all_list:
                url = parse.urljoin(response.url, url)
                # print(url)
                urlitem["url"] = url
                urlitem["creat_time"] = time.strftime("%Y-%m-%d", time.localtime())
                urlitem["flag"] = 0
                urlitem["source_id"] = str(response.meta["source_id"])
                yield urlitem
        elif 'jsonpath:' in response.meta["list_rule"]:
            connect = Operate_datebase_table("adv_spider_list_link")  # 链接文章列表
            urlbase = connect.selectTable("(urlbase)", response.meta["source_id"])  # 查找文章url样式
            response_page = json.loads(response.text)
            import jsonpath
            all_list = jsonpath.jsonpath(response_page, response.meta["list_rule"][8:])
            for url in all_list:
                url = urlbase.format(index=url)
                urlitem["url"] = url
                urlitem["creat_time"] = time.strftime("%Y-%m-%d", time.localtime())
                urlitem["flag"] = 0
                urlitem["source_id"] = str(response.meta["source_id"])
                yield urlitem
            pass
        else:
            pass
        updata_connect = Operate_datebase_table("adv_spider_list_link")  # 链接文章列表
        updata_connect.updateTale({'fetched': '1', }, 'url="{}"'.format(response.url))  # 将该url的fetched位置 1
