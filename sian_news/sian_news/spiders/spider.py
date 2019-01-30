# -*- coding: utf-8 -*-
import scrapy
import json
import time
import hashlib
import redis
from sian_news.settings import COMPANY_FROM, COMPANY_FROM1, ALL
from urllib import parse
from sian_news.items import PageItem
from bs4 import BeautifulSoup
from . import clean, clean_date
import re


class SpiderSpider(scrapy.Spider):
    name = 'spider'

    def get_md5(self, data):
        if isinstance(data, str):
            data = data.encode("utf-8")
        m = hashlib.md5()
        m.update(data)
        return m.hexdigest()

    def redis_push(self, url, company_from):
        r = redis.Redis(host='10.125.0.7', port=6379, db=0, password='crs-hbnwcb9i:r@16samVW!jh',socket_connect_timeout=5)
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

    def redis_push1(self, url, company_from):
        r = redis.Redis(host='10.125.0.7', port=6379, db=0, password='crs-hbnwcb9i:r@16samVW!jh',socket_connect_timeout=5)
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

    def start_requests(self):
        #http://ent.sina.com.cn/rollnews.shtml#pageid=382&lid=2990&k=&num=50&page=1
        for i in range(ALL):
            url = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&k=&num=50&page={}'.format(i)
            yield scrapy.FormRequest(url=url, dont_filter=True, )
            url = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=382&lid=2990&k=&num=50&page={}'.format(i)
            yield scrapy.FormRequest(url=url, dont_filter=True,)

    def parse(self, response):
        response_page = json.loads(response.text)
        response_page = response_page['result']['data']
        if response_page != []:
            for datas in response_page:
                url = datas['url']
                creat_time = datas['ctime']
                media_name = datas['media_name']
                title = datas['title']
                if 'pageid=153' in response.url:
                    yield scrapy.Request(url=url,
                                         dont_filter=True,
                                         callback=self.analysis_page,
                                         meta={
                                             'creat_time': creat_time,
                                             'media_name': media_name,
                                             'title': title,
                                         })
                elif 'pageid=382' in response.url:
                    yield scrapy.Request(url=url,
                                         dont_filter=True,
                                         callback=self.analysis_page1,
                                         meta={
                                             'creat_time': creat_time,
                                             'media_name': media_name,
                                             'title': title,
                                         })
        else:
            pass

    def analysis_page(self, response):
        if response.status == 200:
            item = PageItem()
            url_hash = self.get_md5(response.url)
            title = response.meta['title']
            # media_name = response.meta['media_name']
            creat_time = response.meta['creat_time']
            fetch_time = int(time.time())
            content = response.css('.article').extract()
            if content != []:
                content = content[0]
            else:
                return
            imgs = response.css('.article img::attr(src)').extract()
            source = COMPANY_FROM
            if imgs:
                has_img = 1
                for img in imgs:
                    newimg = parse.urljoin(response.url, img)
                    newUrl = self.redis_push(newimg, COMPANY_FROM)
                    content = content.replace(img, newUrl)
            else:
                has_img = 0
            soup = BeautifulSoup(content, 'lxml')
            clean(soup)
            # print(soup)
            content = str(soup)
            content = clean_date(content)
            content = content.replace("'", '"')
            item['url'] = response.url
            item['url_hash'] = url_hash
            item['title'] = title
            item['content'] = content
            item['creat_time'] = creat_time
            item['fetch_time'] = fetch_time
            item['has_img'] = has_img
            item['source'] = source
            yield item

    def analysis_page1(self, response):
        if response.status == 200:
            item = PageItem()
            url_hash = self.get_md5(response.url)
            title = response.meta['title']
            # media_name = response.meta['media_name']
            creat_time = response.meta['creat_time']
            fetch_time = int(time.time())
            content = response.css('.article').extract()
            if content != []:
                content = content[0]
            else:
                return
            imgs = response.css('.article img::attr(src)').extract()
            source = COMPANY_FROM1
            if imgs:
                has_img = 1
                for img in imgs:
                    newimg = parse.urljoin(response.url, img)
                    newUrl = self.redis_push1(newimg, COMPANY_FROM1)
                    content = content.replace(img, newUrl)
            else:
                has_img = 0
            soup = BeautifulSoup(content, 'lxml')
            clean(soup)
            # print(soup)
            content = str(soup)
            content = clean_date(content)
            content = content.replace("'", '"')
            item['url'] = response.url
            item['url_hash'] = url_hash
            item['title'] = title
            item['content'] = content
            item['creat_time'] = creat_time
            item['fetch_time'] = fetch_time
            item['has_img'] = has_img
            item['source'] = source
            yield item