# -*- coding: utf-8 -*-
import scrapy
try:
    import urlparse as parse
except:
    from urllib import parse
import json
import time
import hashlib
from wangyidingyue.items import YellowurlItem
import redis
from wangyidingyue.settings import COMPANY_FROM


def get_md5(data):
    if isinstance(data, str):
        data = data.encode("utf-8")
    m = hashlib.md5()
    m.update(data)
    return m.hexdigest()


class WangyispiderSpider(scrapy.Spider):
    name = 'wangyispider'
    start_urls = ['http://dy.163.com/v2/index.html/']

    def parse(self, response):
        first_page_urls = response.xpath("//div[@class='nav_content']/ul/li/a/@href|//div[@class='nav_content']/ul/li/a/text()").extract()
        for i in range(0, len(first_page_urls), 2):
            yield scrapy.Request(url=parse.urljoin(response.url, first_page_urls[i]),
                                 meta={
                                     'topic': first_page_urls[i+1]
                                 },
                                 callback=self.get_id_url,
                                 dont_filter=True)

    def get_id_url(self, response):
        id_urls = response.xpath("//ul[@class='column_list clearfix']/li/a/@href").extract()
        for id_url in id_urls:
            id_url = parse.urljoin(response.url, id_url)
            yield scrapy.Request(url=id_url,
                                 meta={
                                     'topic': response.meta['topic']
                                 },
                                 callback=self.get_user_page_url,
                                 dont_filter=True)
        next_get_id_url = response.css("p.award-page.pageList a:last-child::attr(class)").extract_first()
        if next_get_id_url == 'link-lb':
            url = response.css("p.award-page.pageList a:last-child::attr(href)").extract_first()
            yield scrapy.Request(url=parse.urljoin(response.url, url),
                                 meta={
                                     'topic': response.meta['topic']
                                 },
                                 callback=self.get_id_url,
                                 dont_filter=True
                                 )

    def get_user_page_url(self, response):
        wemediaid = response.css("#contain::attr(data-wemediaid)").extract_first()
        url = 'http://dy.163.com/v2/article/list.do?pageNo=1&wemediaId={}&size=1'.format(wemediaid)
        yield scrapy.Request(url=url,
                             meta={
                                 'topic': response.meta['topic'],
                                 'pageNo': 1,
                                 'wemediaid': wemediaid,
                             },
                             callback=self.get_page,
                             dont_filter=True
                             )

    def get_page(self, response):
        # print(response.text)
        data = json.loads(response.text)
        time.sleep(0.5)
        cont = data['data']['list']
        if cont == None:
            pass
        else:
            flag = cont[0]['docid']
            creat_time = cont[0]['showPtime']
            title = cont[0]['title']
            source = cont[0]['source']
            url = 'http://dy.163.com/v2/article/detail/{}.html'.format(flag)
            yield scrapy.Request(url=url,
                                 meta={
                                     'title': title,
                                     'creat_time': creat_time,
                                     'source': source,
                                     'topic': response.meta['topic'],
                                 },
                                 callback=self.analysis_page,
                                 dont_filter=True
                                 )
            next_url = 'http://dy.163.com/v2/article/list.do?pageNo={}&wemediaId={}&size=1'.format(response.meta['pageNo']+1, response.meta['wemediaid'])
            yield scrapy.Request(url=next_url,
                                 meta={
                                     'topic': response.meta['topic'],
                                     'pageNo': response.meta['pageNo']+1,
                                     'wemediaid': response.meta['wemediaid'],
                                 })

    def analysis_page(self, response):
        dataitem = YellowurlItem()

        url = response.url
        url_hash = get_md5(url)
        title = response.meta['title']
        author = response.meta['source']
        topic = response.meta['topic']
        creat_time = response.meta['creat_time']
        if creat_time != "":
            creat_time = time.strptime(str(creat_time), "%Y-%m-%d")
            creat_time = int(time.mktime(creat_time))
        # timeArray = time.strptime(tss1, "%Y-%m-%d")
        content = response.css("#content").extract_first()
        like = response.css("span.fr span a::text").extract_first()
        fetch_time = time.strptime(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "%Y-%m-%d %H:%M:%S")
        fetch_time = int(time.mktime(fetch_time))
        img_url = response.xpath("//div[@id='content']//img/@src").extract()
        if img_url:
            dataitem['has_img'] = 1
            for img in img_url:
                newUrl = self.redis_push(img)
                content = content.replace(img, newUrl)
        else:
            dataitem['has_img'] = 0
        dataitem['url'] = url
        dataitem['url_hash'] = url_hash
        dataitem['title'] = title
        dataitem['author'] = author
        dataitem['topic'] = "网易号"+ topic
        dataitem['creat_time'] = creat_time
        dataitem['content'] = content
        dataitem['like_num'] = like
        dataitem['fetch_time'] = fetch_time
        yield dataitem

    def redis_push(self, url):
        r = redis.Redis(host='10.125.0.7', port=6379, db=0, password='crs-hbnwcb9i:r@16samVW!jh', socket_connect_timeout=5)
        #redis.Redis(host='10.125.0.7', port=6379, db=0, password='crs-hbnwcb9i:r@16samVW!jh',socket_connect_timeout=5)
        # r = redis.Redis(host='127.0.0.1', port=6379, db=0)
        oldUrl = url
        key = get_md5(url)
        fileName = str(key) + '.jpg'
        newUrl = "http://img.market.maizuo.com/" + fileName
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
