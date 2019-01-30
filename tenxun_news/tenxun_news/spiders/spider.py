# -*- coding: utf-8 -*-
import scrapy
import json
from . import clean_date, clean
from bs4 import BeautifulSoup
from urllib import parse
import redis
import hashlib
from tenxun_news.settings import COMPANY_FROM, COMPANY_FROM1, ALL
import time
from tenxun_news.items import PageItem
"""
https://pacaio.match.qq.com/irs/rcd?cid=52&token=8f6b50e1667f130c10f981309e1d8200&ext=101,102,111,113,103,105,106,118,108&page=80,
"""


class SpiderSpider(scrapy.Spider):
    name = 'spider'

    def get_md5(self, data):
        if isinstance(data, str):
            data = data.encode("utf-8")
        m = hashlib.md5()
        m.update(data)
        return m.hexdigest()

    def redis_push(self, url, company_from):
        r = redis.Redis(host='10.125.0.7', port=6379, db=0, password='crs-hbnwcb9i:r@16samVW!jh', socket_connect_timeout=5)
        #redis.Redis(host='10.125.0.7', port=6379, db=0, password='crs-hbnwcb9i:r@16samVW!jh',socket_connect_timeout=5)
        # r = redis.Redis(host='127.0.0.1', port=6379, db=0)
        oldUrl = url
        key = self.get_md5(url)
        fileName = str(key) + '.jpg'
        newUrl = "https://market-1257914648.cos.ap-guangzhou.myqcloud.com/doc_3/" + fileName
        source = company_from
        data = {
            'fileName': fileName,
            'oldUrl': oldUrl,
            'newUrl': newUrl,
            'sourceName': source,
        }
        json_data = json.dumps(data)
        r.lpush('IMG_ALI_OSS', json_data)
        return newUrl

    def redis_push1(self, url, company_from):
        r = redis.Redis(host='10.125.0.7', port=6379, db=0, password='crs-hbnwcb9i:r@16samVW!jh', socket_connect_timeout=5)
        #redis.Redis(host='10.125.0.7', port=6379, db=0, password='crs-hbnwcb9i:r@16samVW!jh',socket_connect_timeout=5)
        # r = redis.Redis(host='127.0.0.1', port=6379, db=0)
        oldUrl = url
        key = self.get_md5(url)
        fileName = str(key) + '.jpg'
        newUrl = "https://market-1257914648.cos.ap-guangzhou.myqcloud.com/doc_2/" + fileName
        source = company_from
        data = {
            'fileName': fileName,
            'oldUrl': oldUrl,
            'newUrl': newUrl,
            'sourceName': source,
        }
        json_data = json.dumps(data)
        r.lpush('IMG_ALI_OSS', json_data)
        return newUrl

    def start_requests(self):
        url = 'https://pacaio.match.qq.com/irs/rcd?cid=52&token=8f6b50e1667f130c10f981309e1d8200&ext=101,102,111,113,103,105,106,118,108&page={index}'
        for i in range(1, ALL+1):
            yield scrapy.Request(url=url.format(index=i),
                                 dont_filter=True,
                                 )
        url = 'https://pacaio.match.qq.com/irs/rcd?cid=108&ext=&token=349ee24cdf9327a050ddad8c166bd3e3&page={index}'
        for i in range(10):
            yield scrapy.Request(url=url.format(index=i),
                                 dont_filter=True,
                                 )

    def parse(self, response):
        response_page = json.loads(response.text)
        if response_page['datanum'] != 0:
            for data in response_page['data']:
                url = data['vurl']
                title = data['title']
                creat_time = data['ts']
                if 'cid=108' in response.url:
                    yield scrapy.Request(url=url,
                                         meta={
                                             'title': title,
                                             'creat_time': creat_time,
                                         },
                                         dont_filter=True,
                                         callback=self.analysis_page1, )
                else:
                    yield scrapy.Request(url=url,
                                         meta={
                                             'title': title,
                                             'creat_time': creat_time,
                                         },
                                         dont_filter=True,
                                         callback=self.analysis_page,)
        else:
            pass
    def analysis_page(self,response):
        content = response.css('div.content-article').extract_first()
        if content != '':
            soup = BeautifulSoup(content, 'lxml')
            imgs = soup.find_all('img')
            if imgs == []:
                has_img = 0
            else:
                has_img = 1
                for img in imgs:
                    newimg = parse.urljoin(response.url, img['src'])
                    newUrl = self.redis_push(newimg, COMPANY_FROM)
                    img['src'] = newUrl
            clean(soup)
            content = str(soup)
            content = clean_date(content)
            content = content.replace("'", '"')
            title = response.meta['title']
            creat_time = response.meta['creat_time']
            fetch_time = int(time.time())
            url = response.url
            url_hash = self.get_md5(url)

            item = PageItem()
            item['url'] = url
            item['url_hash'] = url_hash
            item['has_img'] = has_img
            item['title'] = title
            item['content'] = content
            item['creat_time'] = creat_time
            item['fetch_time'] = fetch_time
            item['source'] = COMPANY_FROM
            yield item
        else:
            pass

    def analysis_page1(self, response):
        content = response.css('div.content-article').extract_first()
        if content != '':
            soup = BeautifulSoup(content, 'lxml')
            imgs = soup.find_all('img')
            if imgs == []:
                has_img = 0
            else:
                has_img = 1
                for img in imgs:
                    newimg = parse.urljoin(response.url, img['src'])
                    newUrl = self.redis_push1(newimg, COMPANY_FROM)
                    img['src'] = newUrl
            clean(soup)
            content = str(soup)
            content = clean_date(content)
            content = content.replace("'", '"')
            title = response.meta['title']
            creat_time = response.meta['creat_time']
            fetch_time = int(time.time())
            url = response.url
            url_hash = self.get_md5(url)

            item = PageItem()
            item['url'] = url
            item['url_hash'] = url_hash
            item['has_img'] = has_img
            item['title'] = title
            item['content'] = content
            item['creat_time'] = creat_time
            item['fetch_time'] = fetch_time
            item['source'] = COMPANY_FROM1
            yield item
        else:
            pass