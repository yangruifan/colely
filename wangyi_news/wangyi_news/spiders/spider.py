# -*- coding: utf-8 -*-
import scrapy
import json
from . import clean_date, clean
from bs4 import BeautifulSoup
from urllib import parse
import redis
import hashlib
from wangyi_news.settings import COMPANY_FROM
import time
from wangyi_news.items import PageItem
"""
http://ent.163.com/special/000380VU/newsdata_music.js?callback=data_callback
http://ent.163.com/special/000380VU/newsdata_show.js?callback=data_callback
http://ent.163.com/special/000380VU/newsdata_tv.js?callback=data_callback
http://ent.163.com/special/000380VU/newsdata_movie.js?callback=data_callback
http://ent.163.com/special/000380VU/newsdata_star.js?callback=data_callback
"""
class SpiderSpider(scrapy.Spider):
    name = 'spider'

    def get_md5(self, data):
        if isinstance(data, str):
            data = data.encode("utf-8")
        m = hashlib.md5()
        m.update(data)
        return m.hexdigest()

    def redis_push(self, url):
        r = redis.Redis(host='10.125.0.7', port=6379, db=0, password='crs-hbnwcb9i:r@16samVW!jh',socket_connect_timeout=5)
        #redis.Redis(host='10.125.0.7', port=6379, db=0, password='crs-hbnwcb9i:r@16samVW!jh',socket_connect_timeout=5)
        # r = redis.Redis(host='127.0.0.1', port=6379, db=0)
        oldUrl = url
        key = self.get_md5(url)
        fileName = str(key) + '.jpg'
        newUrl = "https://market-1257914648.cos.ap-guangzhou.myqcloud.com/doc_3/" + fileName
        source = COMPANY_FROM
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
        urls = ['http://ent.163.com/special/000380VU/newsdata_music{}.js?callback=data_callback',
                'http://ent.163.com/special/000380VU/newsdata_show{}.js?callback=data_callback',
                'http://ent.163.com/special/000380VU/newsdata_tv{}.js?callback=data_callback',
                'http://ent.163.com/special/000380VU/newsdata_movie{}.js?callback=data_callback',
                'http://ent.163.com/special/000380VU/newsdata_star{}.js?callback=data_callback',
                ]
        for i in range(1, 11):
            for url in urls:
                if i == 1:
                    yield scrapy.Request(url=url.format(''),
                                         dont_filter=True,
                                         )
                elif i == 10:
                    yield scrapy.Request(url=url.format('_10'),
                                         dont_filter=True,
                                         )
                else:
                    yield scrapy.Request(url=url.format('_0' + str(i)),
                                         dont_filter=True,
                                         )

    def parse(self, response):
        response = str(response.text)[14:-1]
        response_page = json.loads(response)
        for data in response_page:
            url = data['docurl']
            craet_time = data['time']
            title = data['title']
            if url[7:9] == 'dy':
                continue
            else:
                yield scrapy.Request(url=url,
                                     dont_filter=True,
                                     meta={
                                         'creat_time': craet_time,
                                     },
                                     callback=self.analysis_page,)

    def analysis_page(self, response):
        flag = response.css('ul.nph_list_thumb').extract()
        if flag == []:
            content = response.css('div.post_text').extract()[0]

        else:
            content = response.css('div.end-text').extract()[0]

        soup = BeautifulSoup(content, 'lxml')
        imgs = soup.find_all('img')
        if imgs == []:
            has_img = 0
        else:
            has_img = 1
            for img in imgs:
                newimg = parse.urljoin(response.url, img['src'])
                newUrl = self.redis_push(newimg)
                img['src'] = newUrl
                # content = content.replace(str(img), str(newUrl))

        clean(soup)
        content = str(soup)
        content = clean_date(content)
        content = content.replace("'", '"')
        title = response.css('div.post_content_main h1::text').extract_first()

        creat_time = response.meta['creat_time'][6:10]+'-'+response.meta['creat_time'][0:2]+'-'+response.meta['creat_time'][3:5]+' '+response.meta['creat_time'][11:]
        timeArray = time.strptime(creat_time, "%Y-%m-%d %H:%M:%S")
        creat_time = time.mktime(timeArray)
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