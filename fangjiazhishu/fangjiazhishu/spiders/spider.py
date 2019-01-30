# -*- coding: utf-8 -*-
import scrapy
import re
import json
from fangjiazhishu.items import FangjiaItem
import hashlib
import time
from fangjiazhishu.settings import COMPANY_FROM


class SpiderSpider(scrapy.Spider):
    name = 'spider'

    def get_md5(self, data):
        if isinstance(data, str):
            data = data.encode("utf-8")
        m = hashlib.md5()
        m.update(data)
        return m.hexdigest()

    def start_requests(self):
        url = 'https://www.anjuke.com/sy-city.html'
        yield scrapy.Request(url=url, dont_filter=True)

    def parse(self, response):
        if 'antispam' in response.url or response.status == 429:
        # if response.status != 200:
            print(response.status)
            url = 'https://www.anjuke.com/sy-city.html'
            yield scrapy.Request(url=url, dont_filter=True)
        else:
            city_data = response.xpath(
                "//div[@class='letter_city']/ul/li/div/a/@href|//div[@class='letter_city']/ul/li/div/a/text()").extract()
            alllist = []
            for i in range(0, len(city_data), 2):
                city_url = city_data[i]
                city_name = city_data[i + 1]
                # print(city_name, city_url)
                if city_url in alllist:
                    pass
                else:
                    alllist.append(city_url)
                    yield scrapy.Request(url=city_url + '/market/',
                                         meta={
                                             "city_name": city_name,
                                             "city_url": city_url + '/market/',
                                         },
                                         callback=self.analysis_page,
                                         dont_filter=True)

    def analysis_page(self, response):
        if 'antispam' in response.url or 'callback' in response.url or response.status == 429:
        # if response.status != 200:
            print(response.status)
            url = response.meta['city_url']
            yield scrapy.Request(url=url,
                                 meta={
                                     "city_name": response.meta['city_name'],
                                     "city_url": response.meta['city_url'],
                                 },
                                 callback=self.analysis_page,
                                 dont_filter=True)
        else:
            print(response.meta['city_name'], response.meta['city_url'], "请求成功。")
            item = FangjiaItem()
            reg = 'ajk.citySelector.*?xyear:({.*?}),.*?"data":(.*?)}'
            data = re.search(reg, response.text, re.S)
            try:
                date = json.loads(data.group(1))
                data = json.loads(data.group(2))
            except AttributeError as e:
                print("'NoneType' object has no attribute 'group':data 为 None.")
            print(date)
            print(data)
            timess = []
            for key, value in date.items():
                timess.append(str(value) + str(key))
            for tim, num in zip(timess, data):
                item['cityname'] = response.meta['city_name']
                item['cityname_hash'] = self.get_md5(response.meta['city_name'])
                item['url'] = response.meta['city_url']
                item['fetch_time'] = tim.replace('年', '-').replace('月', '')
                item['creat_time'] = time.strftime("%Y-%m-%d", time.localtime())
                item['num'] = num
                item['source'] = COMPANY_FROM
                yield item




            

