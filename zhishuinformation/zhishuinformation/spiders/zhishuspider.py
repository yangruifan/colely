# -*- coding: utf-8 -*-
import scrapy
import json
#from zhishuinformation.commom import get_cookies,get_md5
import time
from zhishuinformation.items import YellowurlItem, YeItem, YellItem, Diquitem
from zhishuinformation.settings import COMPANY_FROM
import re
import datetime
import redis
import hashlib
from zhishuinformation.city_daihao import CITY_NAME, PROVINCES
NUM = 1
REDISDBNAME = 'baiduCookies'


class ZhishuspiderSpider(scrapy.Spider):
    name = 'zhishuspider'

    def __init__(self, word):
        self.word = word
        self.redis_dbname = REDISDBNAME

    def sleeps(self):
        time.sleep(NUM)

    def get_md5(self,data):
        if isinstance(data, str):
            data = data.encode("utf-8")
        m = hashlib.md5()
        m.update(data)
        return m.hexdigest()

    def reget_cookies(self):
        # get_cookie = get_cookies()
        # get_cookie.get_cookie()
        # get_cookie.close_driver()
        # with open("./cookies.txt", 'r') as f:
        #     cookies = f.read()
        # self.cookies = json.loads(cookies)
        r = redis.Redis(host='10.125.0.7', port=6379, db=0, password='crs-hbnwcb9i:r@16samVW!jh', socket_connect_timeout=5)
        # redis.Redis(host='10.125.0.7', port=6379, db=0, password='crs-hbnwcb9i:r@16samVW!jh',socket_connect_timeout=5)
        # r = redis.Redis(host='127.0.0.1', port=6379, db=0)
        cookies = r.rpoplpush(self.redis_dbname, self.redis_dbname)
        # print(cookies)
        self.cookies = [json.loads(cookies), ]

    def delete_cookies(self):
        r = redis.Redis(host='10.125.0.7', port=6379, db=0, password='crs-hbnwcb9i:r@16samVW!jh', socket_connect_timeout=5)
        # redis.Redis(host='10.125.0.7', port=6379, db=0, password='crs-hbnwcb9i:r@16samVW!jh',socket_connect_timeout=5)
        # r = redis.Redis(host='127.0.0.1', port=6379, db=0)
        r.lpop(self.redis_dbname)

    def start_requests(self):
        """
        从cookies.txt文本文件中获得cookies，
        请求百度API接口尝试连接。
        :return:
        """

        # with open("./cookies.txt", 'r') as f:
        #     cookies = f.read()
        #     if cookies == '':
        #         self.reget_cookies()
        #         with open("./cookies.txt", 'r') as fb:
        #             cookies = fb.read()
        # self.cookies = json.loads(cookies)
        self.reget_cookies()
        # 注：搜索指数整体日均值
        falg = datetime.datetime.now().strftime('%Y-%m-%d')
        url = 'http://index.baidu.com/api/SearchApi/index?word={}&days=1'.format(self.word)
        yield scrapy.Request(url=url, meta={'flag': falg, 'type': '1'}, cookies=self.cookies)
        # url = 'http://index.baidu.com/Interface/Newwordgraph?word={}'.format(self.word)
        # self.sleeps()
        # self.reget_cookies()
        # yield scrapy.Request(url=url, meta={'flag': falg, 'type': '5'}, cookies=self.cookies,
        #                      callback=self.analysis_4page)

    def parse(self, response):
        """
        zhishuitem['date'] 搜索日期
        zhishuitem['allavg'] 全部指数
        zhishuitem['pcavg'] PC端指数
        zhishuitem['wiseavg'] 移动端指数
        zhishuitem['flag'] 标志位 判断是什么时间爬取的
        zhishuitem['sql_flag'] sql标志位
        zhishuitem['name'] 关键字
        zhishuitem['name_hash'] 关键字哈希
        :param response:
        :return:
        """
        response_page = json.loads(response.text)
        if response_page['message'] == 'not login':
            print("没有有效登陆Cookies,请重新获取Cookies.")
            self.delete_cookies()
            self.reget_cookies()
            self.sleeps()
            yield scrapy.Request(url=response.url, meta={'flag': response.meta['flag'], 'type': '1'}, cookies=self.cookies)
        else:
            print("登陆成功！")
            try:
                fetch_time = datetime.datetime.now().strftime('%Y-%m-%d')
                zhishuitem = YellowurlItem()
                date = response_page['data']['userIndexes'][0]['all']['startDate'] # 请求的日期
                allavg = response_page['data']['generalRatio'][0]['all']['avg'] # 当天所有的指数
                pcavg = response_page['data']['generalRatio'][0]['pc']['avg'] # 当天PC端的请求指数
                wiseavg = response_page['data']['generalRatio'][0]['wise']['avg'] # 当天手机端的请求指数
                flag = response.meta['flag']
                zhishuitem['date'] = date
                zhishuitem['allavg'] = allavg
                zhishuitem['pcavg'] = pcavg
                zhishuitem['wiseavg'] = wiseavg
                zhishuitem['flag'] = flag
                zhishuitem['sql_flag'] = response.meta['type']
                zhishuitem['name'] = self.word
                zhishuitem['name_hash'] = self.get_md5(self.word)
                zhishuitem['source'] = COMPANY_FROM
                zhishuitem['creat_time'] = fetch_time
                yield zhishuitem
            except:
                print("《{}》没有指数信息。".format(self.word))
            # 注：资讯指数日均值
            url = 'http://index.baidu.com/api/FeedSearchApi/getFeedIndex?word={}&days=1'.format(self.word)
            self.sleeps()
            self.reget_cookies()
            yield scrapy.Request(url=url, meta={'flag': response.meta['flag'], 'type': '2'}, cookies=self.cookies, callback=self.analysis_1page)

    def analysis_1page(self, response):
        response_page = json.loads(response.text)
        if response_page['message'] == 'not login':
            print("没有有效登陆Cookies,请重新获取Cookies.")
            self.delete_cookies()
            self.reget_cookies()
            self.sleeps()
            yield scrapy.Request(url=response.url, meta={'flag': response.meta['flag'], 'type': '2'}, cookies=self.cookies, callback=self.analysis_1page)
        else:
            print("登陆成功！")
            try:
                fetch_time = datetime.datetime.now().strftime('%Y-%m-%d')
                zhishuitem = YellowurlItem()
                date = response_page['data']['index'][0]['startDate']
                avg = response_page['data']['index'][0]['generalRatio']['avg']
                flag = response.meta['flag']
                zhishuitem['name'] = self.word
                zhishuitem['avg'] = avg
                zhishuitem['flag'] = flag
                zhishuitem['sql_flag'] = response.meta['type']
                zhishuitem['creat_time'] = fetch_time
                yield zhishuitem
            except:
                print("《{}》没有资讯指数信息。".format(self.word))
            # 注：全国地址指数分布（response中prov中的数字代表某个省份）
            url = 'http://index.baidu.com/api/SearchApi/region?region=0&word={}&days=1'.format(self.word)
            self.sleeps()
            self.reget_cookies()
            yield scrapy.Request(url=url, meta={'flag': response.meta['flag'], 'type': '3'}, cookies=self.cookies, callback=self.analysis_2page)

    def analysis_2page(self, response):
        response_page = json.loads(response.text)
        if response_page['message'] == 'not login':
            print("没有有效登陆Cookies,请重新获取Cookies.")
            self.delete_cookies()
            self.reget_cookies()
            self.sleeps()
            yield scrapy.Request(url=response.url, meta={'flag': response.meta['flag'], 'type': '3'}, cookies=self.cookies, callback=self.analysis_2page)

        else:
            print("登陆成功！")
            # try:
            # zhishuitem = YellowurlItem()

            # zhishuitem['countrydata'] = "'"+json.dumps(countrydata)+"'"
            # zhishuitem['flag'] = flag
            # zhishuitem['sql_flag'] = response.meta['type']
            # yield zhishuitem
            try:
                item = Diquitem()
                fetch_time = datetime.datetime.now().strftime('%Y-%m-%d')
                if response_page['status'] == 0:
                    date = response_page['data']['region'][0]['period']
                    countrydata = response_page['data']['region'][0]['prov']
                    citydata = response_page['data']['region'][0]['city']
                    flag = response.meta['flag']
                    billboard = response_page['data']['region'][0]['areaName']
                    movie_hash = self.get_md5(self.word)
                    if countrydata != []:
                        for key, value in countrydata.items():
                            item['date'] = date
                            item['region'] = PROVINCES[key]
                            item['regionnum'] = key
                            item['fetch_time'] = fetch_time
                            item['indexs'] = value
                            item['movie'] = self.word
                            item['movie_hash'] = movie_hash
                            item['source'] = COMPANY_FROM
                            item['billboard'] = billboard
                            item['sql_flag'] = response.meta['type']
                            yield item
                            url = 'http://index.baidu.com/api/SearchApi/region?region={0}&word={1}&days=1'.format(key, self.word)
                            self.sleeps()
                            self.reget_cookies()
                            yield scrapy.Request(url=url, meta={'type': '3'}, cookies=self.cookies,
                                                 callback=self.get_Detailed_diqu,)
                    if citydata != []:
                        for key, value in citydata.items():
                            item['date'] = date
                            item['region'] = PROVINCES[key]
                            item['regionnum'] = key
                            item['fetch_time'] = fetch_time
                            item['indexs'] = value
                            item['movie'] = self.word
                            item['movie_hash'] = movie_hash
                            item['source'] = COMPANY_FROM
                            item['billboard'] = billboard
                            yield item
            except:
                print("《{}》没有全国分布指数信息。".format(self.word))
            # # 注：广东省地区的指数分布（response中prov中的数字代表某个市区）
            # url = 'http://index.baidu.com/api/SearchApi/region?region=913&word={}&days=1'.format(self.word)
            # self.sleeps()
            # self.reget_cookies()
            # yield scrapy.Request(url=url, meta={'flag': response.meta['flag'], 'type': '4'}, cookies=self.cookies, callback=self.analysis_3page)
            # 注：需求图谱
            url = 'http://index.baidu.com/Interface/Newwordgraph?word={}'.format(self.word)
            self.sleeps()
            self.reget_cookies()
            yield scrapy.Request(url=url, meta={'flag': response.meta['flag'], 'type': '5'}, cookies=self.cookies,
                                     callback=self.analysis_4page)

    # def analysis_3page(self, response):
    #     response_page = json.loads(response.text)
    #     if response_page['message'] == 'not login':
    #         print("没有有效登陆Cookies,请重新获取Cookies.")
    #         self.delete_cookies()
    #         self.reget_cookies()
    #         self.sleeps()
    #         yield scrapy.Request(url=response.url, meta={'flag': response.meta['flag'], 'type': '4'}, cookies=self.cookies, callback=self.analysis_3page)
    #
    #     else:
    #         print("登陆成功！")
    #         try:
    #             zhishuitem = YellowurlItem()
    #             date = response_page['data']['region'][0]['period']
    #             citydata = response_page['data']['region'][0]['city']
    #             flag = response.meta['flag']
    #             zhishuitem['citydata'] = "'"+json.dumps(citydata)+"'"
    #             zhishuitem['flag'] = flag
    #             zhishuitem['sql_flag'] = response.meta['type']
    #             yield zhishuitem
    #         except:
    #             print("《{}》没有广东城市分布指数信息。".format(self.word))
    #         # 注：需求图谱
    #         url = 'http://index.baidu.com/Interface/Newwordgraph?word={}'.format(self.word)
    #         self.sleeps()
    #         self.reget_cookies()
    #         yield scrapy.Request(url=url, meta={'flag': response.meta['flag'], 'type': '5'}, cookies=self.cookies,
    #                              callback=self.analysis_4page)

    def analysis_4page(self, response):
        response_page = json.loads(response.text)
        if response_page['message'] == 'not login':
            print("没有有效登陆Cookies,请重新获取Cookies.")
            self.delete_cookies()
            self.reget_cookies()
            self.sleeps()
            yield scrapy.Request(url=response.url, meta={'flag': response.meta['flag'], 'type': '5'},
                                 cookies=self.cookies, callback=self.analysis_4page)
        else:
            print("登陆成功！")
            try:
                item = YeItem()
                data = response_page['data']
                # print(data)
                for key, value in data.items():
                    for one_data in value:
                        # print(one_data)
                        link_name = re.search("(.*?)\t.*", one_data).group(1)
                        No0 = self.None_or_noNone(re.search(".*?\t.*?0=([0-9]{1,8}).*?", one_data))
                        No1 = self.None_or_noNone(re.search(".*?\t.*?1=([0-9]{1,8}).*?", one_data))
                        No2 = self.None_or_noNone(re.search(".*?\t.*?2=([0-9]{1,8}).*?", one_data))
                        No3 = self.None_or_noNone(re.search(".*?\t.*?3=([0-9]{1,8}).*?", one_data))
                        No4 = self.None_or_noNone(re.search(".*?\t.*?4=([0-9]{1,8}).*?", one_data))
                        item['name'] = self.word
                        item['name_hash'] = self.get_md5(self.word)
                        item['sql_flag'] = response.meta['type']
                        item['date'] = key
                        item['run_time'] = time.strftime("%Y-%m-%d", time.localtime())
                        item['flag'] = response.meta['flag']
                        item['sql_flag'] = response.meta['type']
                        item['link_name'] = link_name
                        item['No0'] = No0
                        item['No1'] = No1
                        item['No2'] = No2
                        item['No3'] = No3
                        item['No4'] = No4
                        item['source'] = 1
                        yield item
                        # 注：需求图谱
            except:
                print("《{}》没有相关字指数信息。".format(self.word))
        now = datetime.datetime.now()
        delta = datetime.timedelta(days=-31)
        n_days = now + delta
        url = 'http://index.baidu.com/api/SocialApi/getSocial?wordlist[]={}&startdate={}&enddate={}'.format(self.word, n_days.strftime('%Y-%m-%d').replace('-', ''), now.strftime('%Y-%m-%d').replace('-',''))
        self.sleeps()
        self.reget_cookies()
        yield scrapy.Request(url=url, meta={'flag': response.meta['flag'], 'type': '6'},
                             cookies=self.cookies,
                             callback=self.analysis_5page)

    def None_or_noNone(self, data):
        if data == None:
            data = 0
        else:
            data = data.group(1)
        return data

    def analysis_5page(self, response):
        response_page = json.loads(response.text)
        if response_page['message'] == 'not login':
            print("没有有效登陆Cookies,请重新获取Cookies.")
            self.delete_cookies()
            self.reget_cookies()
            self.sleeps()
            yield scrapy.Request(url=response.url, meta={'flag': response.meta['flag'], 'type': '6'},
                                 cookies=self.cookies, callback=self.analysis_5page)
        else:
            print("登陆成功！")
            try:
                item = YellItem()
                data = response_page['data'][0]
                date = data['period']
                before_nineteen = data['str_age']['1']
                twenty_to_thirty = data['str_age']['2']
                thirty_to_forty = data['str_age']['3']
                forty_to_fifty = data['str_age']['4']
                aften_fifty = data['str_age']['5']
                men = data['str_sex']['M']
                women = data['str_sex']['F']
                item['before_nineteen'] = before_nineteen
                item['twenty_to_thirty'] = twenty_to_thirty
                item['thirty_to_forty'] = thirty_to_forty
                item['forty_to_fifty'] = forty_to_fifty
                item['aften_fifty'] = aften_fifty
                item['men'] = men
                item['women'] = women
                item['flag'] = response.meta['flag']
                item['sql_flag'] = response.meta['type']
                item['date'] = date
                item['name'] = self.word
                item['name_hash'] = self.get_md5(self.word)
                item['source'] = COMPANY_FROM
                yield item

            except:
                print("《{}》没有年龄性别分布指数信息。".format(self.word))

    # 后期追加（更加详细的地区分布指数获取）
    def get_Detailed_diqu(self, response):
        response_page = json.loads(response.text)
        if response_page['message'] == 'not login':
            print("没有有效登陆Cookies,请重新获取Cookies.")
            self.delete_cookies()
            self.reget_cookies()
            self.sleeps()
            yield scrapy.Request(url=response.url,
                                 meta={'type': '3'},
                                 cookies=self.cookies,
                                 callback=self.get_Detailed_diqu,)
        else:
            print("登陆成功！")
            item = Diquitem()
            fetch_time = datetime.datetime.now().strftime('%Y-%m-%d')
            date = response_page['data']['region'][0]['period']
            countrydata = response_page['data']['region'][0]['city']
            if response_page['status'] == 0:
                billboard = response_page['data']['region'][0]['areaName']
                if countrydata != []:
                    for key, value in countrydata.items():
                        item['date'] = date
                        item['region'] = CITY_NAME[key]
                        item['regionnum'] = key
                        item['fetch_time'] = fetch_time
                        item['indexs'] = value
                        item['movie'] = self.word
                        item['movie_hash'] = self.get_md5(self.word)
                        item['source'] = COMPANY_FROM
                        item['billboard'] = billboard
                        item['sql_flag'] = response.meta['type']
                        yield item