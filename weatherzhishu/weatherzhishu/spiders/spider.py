# -*- coding: utf-8 -*-
import scrapy
import json
import datetime
from weatherzhishu.items import WeatherItem
from weatherzhishu.settings import COMPANY_FROM



class SpiderSpider(scrapy.Spider):
    name = 'spider'

    def start_requests(self):

            # url = "http://www.weather.com.cn/data/city3jdata/china.html"
            url = "http://qh.weather.com.cn/data/city3jdata/china.html"
            yield scrapy.Request(
                url=url,
                meta={
                    'handle_httpstatus_all': True,
                },
                dont_filter=True,)

    def parse(self, response):
        """
        获取省级地区的代码号并发送请求
        :param response:
        :return:
        """
        if response.status == 200:
            response_page = json.loads(response.text)
            for i in range(1, 35):
                if i < 10:
                    i = "0" + str(i)
                else:
                    i = str(i)
                num = "101" + i
                province = response_page[num]
                # url = 'http://www.weather.com.cn/data/city3jdata/provshi/{}.html'.format(num)
                url = 'http://qh.weather.com.cn/data/city3jdata/provshi/{}.html'.format(num)
                yield scrapy.Request(url=url,
                                     meta={
                                         'province': province,
                                         'num': num,
                                         'handle_httpstatus_all': True,
                                     },
                                     callback=self.next_parse,
                                     dont_filter=True)
        else:
            print(response.status, '错误代码号')
            yield scrapy.Request(
                url=response.url,
                meta={
                    'handle_httpstatus_all': True,
                },
                dont_filter=True, )


    def next_parse(self, response):
        """
        获取市级地区的代码号并请求
        且判断当市级代码号只有 00 代码号的时候，返回到one_classpage函数
        当市级代码号是 01、02、03等的时候，返回到two_classpage函数
        :param response:
        :return:
        """
        if response.status == 200:
            response_page = json.loads(response.text)
            for key, value in response_page.items():
                city = value
                # url = 'http://www.weather.com.cn/data/city3jdata/station/{0}{1}.html'.format(response.meta['num'], key)
                url = 'http://qh.weather.com.cn/data/city3jdata/station/{0}{1}.html'.format(response.meta['num'], key)
                if key == '00':
                    yield scrapy.Request(
                        url=url,
                        meta={
                            'city': city,
                            'province': response.meta['province'],
                            'num': response.meta['num'],
                            'numson': key,
                            'handle_httpstatus_all': True,
                        },
                        callback=self.oneclass_page,
                        dont_filter=True)
                else:
                    yield scrapy.Request(
                        url=url,
                        meta={
                            'city': city,
                            'province': response.meta['province'],
                            'num': response.meta['num'],
                            'numson': key,
                            'handle_httpstatus_all': True,
                        },
                        callback=self.twoclass_page,
                        dont_filter=True)
        else:
            print(response.status, '错误代码号')
            yield scrapy.Request(
                url=response.url,
                meta={
                    'handle_httpstatus_all': True,
                    'province': response.meta['province'],
                    'num': response.meta['num'],
                },
                dont_filter=True,
                callback=self.next_parse,)

    def oneclass_page(self, response):
        """
        拼接完整正确的url并请求
        :param response:
        :return:
        """
        if response.status == 200:
            response_page = json.loads(response.text)
            for key, value in response_page.items():
                county = value
                num = response.meta['num'] + key + response.meta['numson']
                url = 'http://www.weather.com.cn/weather1d/{0}{1}{2}.shtml'.format(response.meta['num'], key, response.meta['numson'])
                # url = 'http://www.weather.com.cn/weather1dn/101130108.shtml'
                if len(key) > 4:
                    url = 'http://www.weather.com.cn/weather1d/{0}.shtml'.format(key)
                    num = key
                yield scrapy.Request(url=url,
                                     meta={
                                         'county': county,
                                         'city': response.meta['city'],
                                         'province': response.meta['province'],
                                         'daihao': num,
                                     },
                                     callback=self.annlysis_page,
                                     dont_filter=True)
        # elif response.status == 429:
        #     print(response.status, '错误代码号')
        else:
            print(response.status, '错误代码号')
            yield scrapy.Request(
                url=response.url,
                meta={
                    'handle_httpstatus_all': True,
                    'city': response.meta['city'],
                    'province': response.meta['province'],
                    'num': response.meta['num'],
                    'numson': response.meta['numson'],
                },
                dont_filter=True,
                callback=self.oneclass_page,)

    def twoclass_page(self, response):
        """
        拼接完整正确的url并请求
        :param response:
        :return:
        """
        if response.status == 200:
            response_page = json.loads(response.text)
            for key, value in response_page.items():
                county = value
                num = response.meta['num'] + response.meta['numson'] + key
                url = 'http://www.weather.com.cn/weather1d/{0}{1}{2}.shtml'.format(response.meta['num'],
                                                                                        response.meta['numson'],
                                                                                        key)
                # url = 'http://www.weather.com.cn/weather1dn/101130108.shtml'
                if len(key) > 4:
                    url = 'http://www.weather.com.cn/weather1d/{0}.shtml'.format(key)
                    num = key
                yield scrapy.Request(url=url,
                                     meta={
                                         'handle_httpstatus_all': True,
                                         'county': county,
                                         'city': response.meta['city'],
                                         'province': response.meta['province'],
                                         'daihao': num,
                                     },
                                     callback=self.annlysis_page,
                                     dont_filter=True)
        # elif response.status == 429:
        #     print(response.status, '错误代码号')
        else:
            print(response.status, '错误代码号')
            yield scrapy.Request(
                url=response.url,
                meta={
                    'handle_httpstatus_all': True,
                    'city': response.meta['city'],
                    'province': response.meta['province'],
                    'num': response.meta['num'],
                    'numson': response.meta['numson'],
                },
                dont_filter=True,
                callback=self.twoclass_page)

    def annlysis_page(self, response):
        """
        运用xpath函数定位信息
        :param response:
        :return:
        """
        if response.status == 200:
            weatheritem = WeatherItem()
            # names = response.xpath("//div[@class='weather_shzs weather_shzs_1d']/ul/li/h2/text()").extract()
            # zhishus = response.xpath("//div[@class='lv']/dl/dt/em/text()|//div[@class='lv']/dl/dd/text()").extract()
            # # reg = "([\u4e00-\u9fa5]{1,8})"
            datas = response.xpath("//div[@class='livezs']/ul/li/span/text()|//div[@class='livezs']/ul/li/em/text()|//div[@class='livezs']/ul/li/p/text()").extract()
            for i in range(0, len(datas), 3):
                name = datas[i+1].replace('健臻·','')
                zhishu = datas[i]
                zhishu_details = datas[i + 2]
                county = response.meta['county']
                areanum = response.meta['daihao']
                city = response.meta['city']
                province = response.meta['province']
                fetch_time = datetime.datetime.now().strftime('%Y-%m-%d')
                url = response.url
                weatheritem['num'] = str(i//3+1)
                weatheritem['name'] = name
                weatheritem['zhishu'] = zhishu
                weatheritem['zhishu_details'] = zhishu_details
                weatheritem['cityname'] = city
                weatheritem['areaname'] = county
                weatheritem['provincename'] = province
                weatheritem['fetch_time'] = fetch_time
                weatheritem['url'] = url
                weatheritem['areanum'] = areanum
                weatheritem['source'] = COMPANY_FROM
                yield weatheritem
            chuanyi = response.xpath("//li[@id='chuanyi']/a/span/text()|//li[@id='chuanyi']/a/em/text()|//li[@id='chuanyi']/a/p/text()").extract()
            name = chuanyi[1]
            zhishu = chuanyi[0]
            zhishu_details = chuanyi[2]
            county = response.meta['county']
            areanum = response.meta['daihao']
            city = response.meta['city']
            province = response.meta['province']
            fetch_time = datetime.datetime.now().strftime('%Y-%m-%d')
            url = response.url
            weatheritem['num'] = 5
            weatheritem['name'] = name
            weatheritem['zhishu'] = zhishu
            weatheritem['zhishu_details'] = zhishu_details
            weatheritem['cityname'] = city
            weatheritem['areaname'] = county
            weatheritem['provincename'] = province
            weatheritem['fetch_time'] = fetch_time
            weatheritem['url'] = url
            weatheritem['areanum'] = areanum
            weatheritem['source'] = COMPANY_FROM
            yield weatheritem
        # elif response.status == 429:
        #     print(response.status, '错误代码号')
        else:
            print(response.status, '错误代码号')
            yield scrapy.Request(
                url=response.url,
                meta={
                    'handle_httpstatus_all': True,
                    'county': response.meta['county'],
                    'city': response.meta['city'],
                    'province': response.meta['province'],
                    'daihao': response.meta['daihao'],
                },
                dont_filter=True,
                callback=self.annlysis_page)
