# -*- coding: utf-8 -*-
import scrapy
import pymysql
from scrapy.http import Request
try:
    import  urlparse as parse
except:
    from urllib import parse
import time
from baijiahao.untils.commons import get_md5
from baijiahao.items import BaijiahaoItem

class BaijiahaoSpiderSpider(scrapy.Spider):
    name = 'baijiahao_spider'
    allowed_domains = ['www']
    start_urls = []
    headers = {
        'host': "www.baidu.com",
    }
    def start_requests(self):
        # """
        # :return:通过从数据库中获取关键字，进行百度搜索。
        # """

        client = pymysql.connect(host='localhost', port=3306, user='root', passwd='960823', db='scrapy', charset='utf8',
                                 use_unicode=True)
        cursor = client.cursor()
        # SQL 查询语句
        sql = "SELECT distinct name FROM movie_zhishu WHERE topic_parent = '电影'"
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            # print(results)
            for data in results:
                self.start_urls.append(data[0])
        except:
            print("关键字提取失败！")
        # 关闭数据库连接
        client.close()

        for url_son in self.start_urls:
            yield Request(url="http://www.baidu.com/s?wd=site:(baijiahao.baidu.com)《{0}》".format(url_son), meta={"index":url_son}, headers=self.headers, dont_filter=True)
        # return [Request(url="http://www.baidu.com/s?wd=site:(baijiahao.baidu.com)《一出好戏》",
        #               meta={"index": "一出好戏"}, headers=self.headers, dont_filter=True)]

    def parse(self, response):
        """
        :param response:百度搜索结果页面
        :return:1、返回一篇文章的整个页面
                2、实现翻页功能
        """

        ten_page_url = response.css("#content_left div.result h3 a::attr(href)").extract()
        for url in ten_page_url:
            yield Request(url= url, meta={"index":response.meta['index']}, callback=self.analysis_page,dont_filter=True)

        #实现翻页功能
        page_num = response.css("#page strong span:nth-child(2)::text").extract_first()
        if int(page_num) >= 10:
            pass
        else:
            print(page_num)
            last_url = "http://www.baidu.com/s?wd=site:(baijiahao.baidu.com)《{0}》&pn={1}0".format(response.meta['index'],page_num)
            yield Request(url= last_url, meta={"index":response.meta['index']}, headers= self.headers, dont_filter= True)




    def analysis_page(self,response):
        """
        :param response:一篇文章的整个页面
        :return:返回文章中的重要信息
        """

        baijiahaoitem = BaijiahaoItem()
        # print(response.url)
        tittle = response.css("div.article-title h2::text").extract_first()
        tittle_hash = get_md5(tittle)
        author = response.css("div.author-txt p.author-name::text").extract_first()
        if author == '':
            author = '百家号作者'
        source_and_time = response.css("div.author-txt div.article-source span::text").extract()
        spider_time = time.strftime("%Y-%m-%d", time.localtime())
        if source_and_time == '':
            source = '暂无'
            creat_time = 'xx-xx-xx'
        else:
            source = source_and_time[0]
            creat_time = source_and_time[1]+ " "+ source_and_time[2]

            if creat_time[5] != '-':
                creat_time = spider_time[2]+ spider_time[3]+ "-"+ creat_time
        author_desc = response.css("div.author-desc p::text").extract_first()[3:-1]
        if author_desc == '':
            author_desc = '暂无'
        content =  response.css("div.article-content").extract_first()
        content = content.replace("amp;",'')

        baijiahaoitem['url'] = response.url
        baijiahaoitem['name'] = response.meta['index']
        baijiahaoitem['tittle'] = tittle
        baijiahaoitem['tittle_hash'] = tittle_hash
        baijiahaoitem['author'] = author
        baijiahaoitem['author_desc'] = author_desc
        baijiahaoitem['source'] = source
        baijiahaoitem['create_time'] = creat_time
        baijiahaoitem['spider_time'] = spider_time
        baijiahaoitem['content'] = content
        yield baijiahaoitem

