# -*- coding: utf-8 -*-
import scrapy
from reweather_index.settings import MY_SQL1, MY_SQL, COMPANY_FROM
import pymysql
import datetime
from reweather_index.items import WeatherItem
# 3点40分爬动程序


class SpiderSpider(scrapy.Spider):
    name = 'spider'

    def start_requests(self):
        self.db = pymysql.connect(
            **MY_SQL1,
            charset="utf8",
            use_unicode=True)
        self.cursor = self.db.cursor()
        self.dbname = 'report_hot_city'
        self.db1 = pymysql.connect(
            **MY_SQL,
            charset="utf8",
            use_unicode=True)
        self.cursor1 = self.db1.cursor()
        self.dbname1 = 'weather_zhishu'
        sql = """select city from %s where weather_value=%r""" % (self.dbname, -1)
        # 执行sql语句
        self.cursor.execute(sql)
        # 获取所有记录列表
        results = self.cursor.fetchall()
        if not results:
            pass
        else:
            for result in results:
                city = result[0].replace('市', '')
                sql = """select distinct url,province,city,county,countynum from %s where county=%r""" % (self.dbname1, city)
                # 执行sql语句
                self.cursor1.execute(sql)
                # 获取所有记录列表
                urls = self.cursor1.fetchall()
                if not urls:
                    pass
                else:
                    url = urls[0][0]
                    yield scrapy.Request(url=url,
                                         dont_filter=True,
                                         meta={
                                             'handle_httpstatus_all': True,
                                             'village': urls[0][2],
                                             'towns': urls[0][3],
                                             'cityname': urls[0][1],
                                             'daihao': urls[0][4],
                                         },

                                         )

    def parse(self, response):
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
            datas = response.xpath(
                "//div[@class='livezs']/ul/li/span/text()|//div[@class='livezs']/ul/li/em/text()|//div[@class='livezs']/ul/li/p/text()").extract()
            for i in range(0, len(datas), 3):
                name = datas[i + 1].replace('健臻·', '')
                zhishu = datas[i]
                zhishu_details = datas[i + 2]
                village = response.meta['village']
                areanum = response.meta['daihao']
                towns = response.meta['towns']
                cityname = response.meta['cityname']
                fetch_time = datetime.datetime.now().strftime('%Y-%m-%d')
                url = response.url
                weatheritem['num'] = str(i // 3 + 1)
                weatheritem['name'] = name
                weatheritem['zhishu'] = zhishu
                weatheritem['zhishu_details'] = zhishu_details
                weatheritem['cityname'] = towns
                weatheritem['areaname'] = village
                weatheritem['provincename'] = cityname
                weatheritem['fetch_time'] = fetch_time
                weatheritem['url'] = url
                weatheritem['areanum'] = areanum
                weatheritem['source'] = COMPANY_FROM
                yield weatheritem
            chuanyi = response.xpath(
                "//li[@id='chuanyi']/a/span/text()|//li[@id='chuanyi']/a/em/text()|//li[@id='chuanyi']/a/p/text()").extract()
            name = chuanyi[1]
            zhishu = chuanyi[0]
            zhishu_details = chuanyi[2]
            village = response.meta['village']
            areanum = response.meta['daihao']
            towns = response.meta['towns']
            cityname = response.meta['cityname']
            fetch_time = datetime.datetime.now().strftime('%Y-%m-%d')
            url = response.url
            weatheritem['num'] = 5
            weatheritem['name'] = name
            weatheritem['zhishu'] = zhishu
            weatheritem['zhishu_details'] = zhishu_details
            weatheritem['cityname'] = towns
            weatheritem['areaname'] = village
            weatheritem['provincename'] = cityname
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
                    'village': response.meta['village'],
                    'towns': response.meta['towns'],
                    'cityname': response.meta['cityname'],
                    'daihao': response.meta['daihao'],
                },
                dont_filter=True,
                callback=self.parse)
