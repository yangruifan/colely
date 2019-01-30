# -*- coding: utf-8 -*-
import scrapy
import random
from urllib.parse import urlencode
import re, json, hashlib, time,requests


class Safe360spidersSpider(scrapy.Spider):
    name = 'safe360spiders'

    def start_requests(self):
        self.username = '13118801536'
        self.password = '520ncswdmx'
        url = 'http://login.360.cn/?'
        login = {
            'src': 'pcw_360index',
            'from': 'pcw_360index',
            'func': 'jQuery18308678295746512812_1545100277789',
            'o': 'sso',
            'm': 'getToken',
            'userName': self.username,
            '_': '1545100538276',
            'requestScema': 'https',
            'charset': 'UTF-8',
        }
        params = urlencode(login)
        url = url + params
        yield scrapy.Request(url=url,
                             dont_filter=True,
                             )

    def parse(self, response):
        reg = '.*?({.*})'
        data = re.search(reg, response.text).group(1)
        data = json.loads(data)
        if data['errno'] == 0:
            token = data['token']
            url = 'http://login.360.cn/'
            datas = {
                'src': 'pcw_360index',
                'from': 'pcw_360index',
                'charset': 'UTF-8',
                'requestScema': 'https',
                'o': 'sso',
                'm': 'login',
                'lm': '0',
                'captFlag': '1',
                'rtype': 'data',
                'validatelm': '0',
                'isKeepAlive': '1',
                'captchaApp': 'i360',
                'userName': self.username,
                'smDeviceId': '',
                'type': 'normal',
                'account': self.username,
                'password': self.get_md5(self.password),
                'captcha': '',
                'token': token,
                'proxy': 'https://trends.so.com/psp_jump.html',
                'callback': 'QiUserJsonp864784493',
                'func': 'QiUserJsonp864784493',
            }
            yield scrapy.FormRequest(url=url,
                                     formdata=datas,
                                     callback=self.login_YN,
                                     )
        else:
            print("获取Token失败。")

    def get_md5(self, data):
        if isinstance(data, str):
            data = data.encode("utf-8")
        m = hashlib.md5()
        m.update(data)
        return m.hexdigest()

    def login_YN(self, response):
        url = 'http://i.360.cn/?src=pcw_360index'
        yield scrapy.Request(url=url,  callback=self.get_page)

    def get_page(self, response):
        print(response.text)
        pass