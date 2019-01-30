# -*- coding: utf-8 -*-
import scrapy
import json
import time
import datetime
from urllib.parse import urlencode
from xiaofeishuiping.items import XiaofeiItem
from xiaofeishuiping.settings import COMPANY_FROM

class SpiderSpider(scrapy.Spider):
    name = 'spider'

    def start_requests(self):
        url = 'http://data.stats.gov.cn/easyquery.htm?m=getOtherWds&dbcode=fsnd&rowcode=zb&colcode=sj&wds=[]'
        yield scrapy.Request(url=url, dont_filter=True)

    def next_class_url(self, city_code, city_name, next_url):
        datas = {
            'm': 'QueryData',
            'dbcode': 'fsnd',
            'rowcode': 'zb',
            'colcode': 'sj',
        }# A0205
        params = urlencode(datas)
        url = 'http://data.stats.gov.cn/easyquery.htm?' + params + '&wds=[{"wdcode":"reg","valuecode":"' + str(
            city_code) + '"}]&dfwds=[{"wdcode":"zb","valuecode":"' + str(next_url) + '"}{"wdcode": "sj", "valuecode": "LAST5"}]'
        return scrapy.Request(url=url.replace("'", '"'),
                              meta={
                                 'city_name': city_name,
                                 'city_code': city_code,
                             },
                              callback=self.analysis_page, )

    def parse(self, response):
        # 在此处加类型需求的代号
        all_url = ['A0205', 'A0A00', 'A0A02', 'A0A03']

        response_page = json.loads(response.text)
        if response_page['returncode'] == 200:
            data = response_page['returndata']
            if data != []:
                citys_nodes = data[0]['nodes']
                # spider_time = data[1]['nodes'][0]['code']
                datas = {
                    'm': 'QueryData',
                    'dbcode': 'fsnd',
                    'rowcode': 'zb',
                    'colcode': 'sj',
                }  # A0205
                params = urlencode(datas)
                for city_data in citys_nodes:
                    city_code = city_data['code']
                    city_name = city_data['name']
                    for next_url in all_url:
                        url = 'http://data.stats.gov.cn/easyquery.htm?' + params + '&wds=[{"wdcode":"reg","valuecode":"' + str(
                            city_code) + '"}]&dfwds=[{"wdcode":"zb","valuecode":"' + str(
                            next_url) + '"}{"wdcode": "sj", "valuecode": "LAST5"}]'
                        yield scrapy.Request(url=url,
                                             meta={
                                                  'city_name': city_name,
                                                  'city_code': city_code,
                                              },
                                             callback=self.analysis_page, )


    def analysis_page(self, response):
        item = XiaofeiItem()
        citydata = {}
        response_page = json.loads(response.text)
        if response_page['returncode'] == 200:
            data = response_page['returndata']
            if data != None:
                names = data['wdnodes']
                if names != None:
                    names = names[0]['nodes']
                    for name in names:
                        citydata[name['code']] = name['cname']
                # print(len(data['datanodes']))
                    datas = data['datanodes']
                    for data_son in datas:
                        value = data_son['data']['data']
                        code = data_son['wds'][0]['valuecode']
                        times = data_son['wds'][2]['valuecode']
                        class_name = citydata[code]
                        # 分类
                        item['name'] = class_name
                        # 发布的时间
                        item['creat_time'] = times
                        # 指数值与详情
                        item['name_code'] = code
                        # 指数
                        item['indexs'] = value
                        # 爬取时间
                        item['fetch_time'] = datetime.datetime.now().strftime('%Y-%m-%d')
                        # 地区
                        item['city'] = response.meta['city_name']
                        item['city_code'] = response.meta['city_code']
                        # 来源
                        item['source'] = COMPANY_FROM
                        yield item


