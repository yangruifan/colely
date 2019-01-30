# -*- coding: utf-8 -*-
import scrapy
import json
from sougou_spider.items import SougouItem
import hashlib
import datetime
import time


class SpiderSpider(scrapy.Spider):
    name = 'spider'

    def __init__(self, word):
        self.word = word

    def start_requests(self):
        now = datetime.datetime.now()
        delta = datetime.timedelta(days=-2)
        now = now + delta
        startday = now.strftime('%Y-%m-%d')
        date = startday.replace('-', '')
        url = 'http://zhishu.sogou.com/getDateData?kwdNamesStr={}&startDate={}&endDate={}&dataType=SEARCH_ALL'.format(self.word, date, date)
        yield scrapy.Request(url=url, dont_filter=True)

    def parse(self, response):
        try:
            fetch_time = datetime.datetime.now().strftime('%Y-%m-%d')
            sougouitem = SougouItem()
            response_page = json.loads(response.text)
            data = response_page['data']['pvList'][0][0]
            allavg = data['pv']
            date = data['date']
            sougouitem['allavg'] = allavg
            sougouitem['create_time'] = date
            sougouitem['fetch_time'] = fetch_time
            sougouitem['sql_flag'] = '1'
            sougouitem['name'] = self.word
            sougouitem['name_hash'] = self.get_md5(self.word)
            sougouitem['source'] = '搜狗指数'
            sougouitem['flag'] = str(time.time() * 1000000)
            yield sougouitem
        except:
            print("《{}》没有在搜狗没有指数信息。".format(self.word))
        url = response.url[0:-10]+'MEDIA_WECHAT'
        yield scrapy.Request(url=url, callback=self.next_page, dont_filter=True)

    def next_page(self, response):
        try:
            fetch_time = datetime.datetime.now().strftime('%Y-%m-%d')
            sougouitem = SougouItem()
            response_page = json.loads(response.text)
            data = response_page['data']['pvList'][0][0]
            wiseavg = data['pv']
            date = data['date']
            sougouitem['wiseavg'] = wiseavg
            sougouitem['create_time'] = date
            sougouitem['fetch_time'] = fetch_time
            sougouitem['sql_flag'] = '2'
            sougouitem['name'] = self.word
            sougouitem['name_hash'] = self.get_md5(self.word)
            sougouitem['source'] = '搜狗指数'
            yield sougouitem
        except:
            print("《{}》没有在搜狗没有移动端指数信息。".format(self.word))

    def get_md5(self, data):
        if isinstance(data, str):
            data = data.encode("utf-8")
        m = hashlib.md5()
        m.update(data)
        return m.hexdigest()