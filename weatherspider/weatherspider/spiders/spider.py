# -*- coding: utf-8 -*-
import scrapy
import json
import datetime
import re


class SpiderSpider(scrapy.Spider):
    name = 'spider'

    def start_requests(self):

            # url = "http://www.weather.com.cn/data/city3jdata/china.html"
            url = "http://qh.weather.com.cn/data/city3jdata/china.html"
            yield scrapy.Request(url=url, dont_filter=True)

    def parse(self, response):
        """
        获取省级地区的代码号并发送请求
        :param response:
        :return:
        """
        response_page = json.loads(response.text)
        for i in range(1, 35):
            if i < 10:
                i = "0" + str(i)
            else:
                i = str(i)
            num = "101" + i
            cityname = response_page[num]
            # url = 'http://www.weather.com.cn/data/city3jdata/provshi/{}.html'.format(num)
            url = 'http://qh.weather.com.cn/data/city3jdata/provshi/{}.html'.format(num)
            yield scrapy.Request(url=url,
                                 meta={
                                     'cityname': cityname,
                                     'num': num,
                                 },
                                 callback=self.next_parse,
                                 dont_filter=True)

    def next_parse(self, response):
        """
        获取市级地区的代码号并请求
        且判断当市级代码号只有 00 代码号的时候，返回到one_classpage函数
        当市级代码号是 01、02、03等的时候，返回到two_classpage函数
        :param response:
        :return:
        """
        response_page = json.loads(response.text)
        for key, value in response_page.items():
            towns = value
            # url = 'http://www.weather.com.cn/data/city3jdata/station/{0}{1}.html'.format(response.meta['num'], key)
            url = 'http://qh.weather.com.cn/data/city3jdata/station/{0}{1}.html'.format(response.meta['num'], key)
            if key == '00':
                yield scrapy.Request(url=url,
                               meta={
                                   'towns': towns,
                                   'cityname': response.meta['cityname'],
                                   'num': response.meta['num'],
                                   'numson': key,
                               },
                               callback=self.oneclass_page,
                               dont_filter=True)
            else:
                yield scrapy.Request(url=url,
                               meta={
                                   'towns': towns,
                                   'cityname': response.meta['cityname'],
                                   'num': response.meta['num'],
                                   'numson': key,
                               },
                               callback=self.twoclass_page,
                               dont_filter=True)

    def oneclass_page(self, response):
        """
        拼接完整正确的url并请求
        :param response:
        :return:
        """
        response_page = json.loads(response.text)
        for key, value in response_page.items():
            village = value
            num = response.meta['num'] + key + response.meta['numson']
            url = 'http://www.weather.com.cn/weather1d/{0}{1}{2}.shtml'.format(response.meta['num'], key, response.meta['numson'])
            # url = 'http://www.weather.com.cn/weather1dn/101130108.shtml'
            if len(key) > 4:
                url = 'http://www.weather.com.cn/weather1d/{0}.shtml'.format(key)
                num = key
            data = {
                'url': url,
                'village': village,
                'towns': response.meta['towns'],
                'cityname': response.meta['cityname'],
                'daihao': num,
            }
            with open('region.txt', 'a')as f:
                f.write(json.dumps(data) + '\n')


    def twoclass_page(self, response):
        """
        拼接完整正确的url并请求
        :param response:
        :return:
        """
        response_page = json.loads(response.text)
        for key, value in response_page.items():
            village = value
            num = response.meta['num'] + response.meta['numson'] + key
            url = 'http://www.weather.com.cn/weather1d/{0}{1}{2}.shtml'.format(response.meta['num'],
                                                                                    response.meta['numson'],
                                                                                    key)
            # url = 'http://www.weather.com.cn/weather1dn/101130108.shtml'
            if len(key) > 4:
                url = 'http://www.weather.com.cn/weather1d/{0}.shtml'.format(key)
                num = key
            data = {
                'url': url,
                'village': village,
                'towns': response.meta['towns'],
                'cityname': response.meta['cityname'],
                'daihao': num,
            }
            with open('region.txt', 'a')as f:
                f.write(json.dumps(data) + '\n')