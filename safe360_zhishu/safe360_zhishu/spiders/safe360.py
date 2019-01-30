# -*- coding: utf-8 -*-
import scrapy
import re,json
from scrapy.http import Request
from safe360_zhishu.items import Safe360Item
import time
from safe360_zhishu.untils.commons import get_md5
class Safe360Spider(scrapy.Spider):
    name = 'safe360'
    allowed_domains = ['trends.so.com']
    start_urls = ['https://trends.so.com/']

    def parse(self, response):
        lists = response.css("#hotCates::text").extract_first()
        lists = re.findall('{.*?}',lists)
        # print(lists)
        for data in lists:
            data=json.loads(data)
            if data["list"]== []:

                url = "https://trends.so.com/top/list?cate1={0}&cate2=&page=1&size=300".format(data["cate1"])
                # print(url)
                yield Request(url=url, callback=self.analysis_page, dont_filter=True)
            else:
                for son in data["list"]:
                    url = "https://trends.so.com/top/list?cate1={0}&cate2={1}&page=1&size=300".format(data["cate1"],son)
                    # print(url)
                    yield Request(url=url, callback=self.analysis_page, dont_filter=True)


    def analysis_page(self,response):
        safe360 = Safe360Item()

        # datas = response["data"]
        response = json.loads(response.text)
        lists = response["data"]["list"]
        print(len(lists))
        for data in lists:
            safe360["name"] = data["title"]
            safe360["class_type_top1"] = data["cate1"]
            safe360["class_type_top2"] = data["cate2"]
            safe360["safe360_number"] = data["search_index"]
            safe360["name_hash"] = get_md5(data["title"])
            safe360["type"] = "360热搜"
            safe360["create_time"] = time.strftime("%Y-%m-%d", time.localtime())
            yield safe360
