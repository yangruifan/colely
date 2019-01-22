# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
import json
import re
from cbooonew.items import PeerItem
from cbooonew.settings import COMPANY_FROM
import datetime
import hashlib

class SpiderSpider(scrapy.Spider):
    name = 'spider'


    def get_md5(self,data):
        if isinstance(data, str):
            data = data.encode("utf-8")
        m = hashlib.md5()
        m.update(data)
        return m.hexdigest()

    def start_requests(self):
        url = 'http://www.cbooo.cn/movies'
        yield scrapy.Request(url=url,
                             dont_filter=True,)

    def parse(self, response):
        countrylist = response.css("#selArea option::attr(value)").extract()
        self.url1 = 'http://www.cbooo.cn/Mdata/getMdata_movie?'
        data = {
            'area': '',
            'type': '0',
            'year': '0',
            'initial': '全部',
            'pIndex': '1',
        }
        for country in countrylist:
            data['area'] = country
            url = self.url1 + parse.urlencode(data)
            yield scrapy.Request(url=url,
                                 dont_filter=True,
                                 meta={
                                     'area': country,
                                 },
                                 callback=self.analysis,)

    def analysis(self, response):
        data = {
            'area': '',
            'type': '0',
            'year': '0',
            'initial': '全部',
            'pIndex': '1',
        }
        response_page = json.loads(response.text)
        tPage = response_page['tPage']
        if tPage == 0 or tPage == None:
            pass
        else:
            for i in range(1, tPage+1):
                data['area'] = response.meta['area']
                data['pIndex'] = str(i)
                url = self.url1 + parse.urlencode(data)
                yield scrapy.Request(url=url,
                                     dont_filter=True,
                                     callback=self.analysis_page)

    def analysis_page(self, response):
        response_page = json.loads(response.text)
        datas = response_page['pData']
        for data in datas:
            ID = data['ID']
            MovieName = data['MovieName']
            yield scrapy.Request(url='http://www.cbooo.cn/Mdata/getMovieEventAll/?movieid={index}#all'.format(index=ID),
                                 dont_filter=True,
                                 meta={
                                     'MovieName': MovieName,
                                 },
                                 callback=self.analysis_movie)

    def get_time(self, data):
        reg = '(\d{4}-\d{2}-\d{2})'
        date = re.search(reg, data)
        return date.group(1)

    def analysis_movie(self, response):
        if response.text == '该影片暂无营销事件':
            pass
        else:
            item = PeerItem()
            ul = response.xpath("//div[@class='item']/div/ul/li/h5/text()|//div[@class='item']/div/ul/li/div/h4/text()|\
            //div[@class='item']/div/ul/li/div/var/text()|//div[@class='item']/div/ul/li/div/p/a/@href").extract()
            for i in range(0, len(ul), 4):
                event = ul[i]
                title = ul[i+1]
                creat_time = self.get_time(ul[i+2])
                url = ul[i+3]
                page_source = ul[i+2].replace('来源：', '').replace(creat_time, '')

                item['movie'] = response.meta['MovieName']
                item['movie_hash'] = self.get_md5(response.meta['MovieName'])
                item['title'] = title
                item['creat_time'] = creat_time
                item['event'] = event
                item['page_source'] = page_source
                item['url'] = url
                item['url_hash'] = self.get_md5(url)
                item['fetch_time'] = datetime.date.today()
                item['source'] = COMPANY_FROM
                yield item
