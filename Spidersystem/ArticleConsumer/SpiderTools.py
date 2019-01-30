#!/usr/bin/env python
# encoding:utf-8
# @Time   : 2018/12/18
# @File   : settings.py

import time
import re
import hashlib
import random
import pymysql
import config
import json
import html
import requests
import redis


class spiderTools(object):
    def __init__(self):
        self.conn = pymysql.connect(**config.mysqlconf)
        self.cursor = self.conn.cursor()
        self.ipRedis = redis.Redis(**config.ipRedisConf)
        self.imgRedis = redis.Redis(**config.imgRedisConf)
        self.typedict = {}

    def getHeader(self):
        """
        获得随机请求头
        :return:
        """
        useragentlist = [
            'Mozilla / 5.0(Macintosh;U;IntelMacOSX10_6_8;en - us) AppleWebKit / 534.50(KHTML, likeGecko) Version / 5.1Safari / 534.50',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
            'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
            'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
            'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        ]
        header = {'User-Agent': random.choice(useragentlist)}
        return header

    def getProxy(self):
        """
        获取代理ip拼接指定的代理格式
        :return:
        """
        ip = self.ipRedis.get('ip').decode()
        proxy = {
            "http" : "http://" + ip,
            "https": "https://" + ip
        }
        return proxy

    def md5(self, inpurtstr):
        """
        对指定字符串进行md5运算
        :param inpurtstr:需要MD5的字符串
        :return:
        """
        h1 = hashlib.md5()
        h1.update(inpurtstr.encode(encoding='utf-8'))
        hash = h1.hexdigest()
        return hash

    def hasSpidered(self, hashedstr):
        """
        链接是否爬取过
        :param hashstr:hash过的url
        :return:
        """
        if len(hashedstr) != 32:
            hashedstr = self.md5(hashedstr)
        self.cursor.execute("select id from spider_posts where hash='{0}'".format(hashedstr))
        data = self.cursor.fetchall()
        if data:
            return True
        return False

    def getHomeImageUrl(self, imgurl, source):
        """
        将网页图片链接转成我司链接
        :param imgurl:网页图片链接
        :param source:数据源名称
        :return:我司图片链接
        """
        filename = self.md5(imgurl) + '.jpg'
        sourcetype = self.typedict.get(source, '')
        if sourcetype=='':
            self.cursor.execute("select type from spider_source_type where source_name='{0}'".format(source))
            sourcetype = self.cursor.fetchall()
            if sourcetype:
                sourcetype = str(sourcetype[0][0])
                self.typedict[source]=sourcetype
            else:
                return ""
        newurl = "https://market-1257914648.cos.ap-guangzhou.myqcloud.com/doc_" + sourcetype + '/' + filename
        return newurl

    def getImgUrls(self, content_text):
        imgurls = re.findall(r'<img.*?src="(.*?)".*?>', content_text)
        return imgurls

    def saveImage(self, imgurl='', source=''):
        """
        图片链接信息入redis库
        :param imgurl:图片链接
        :param source:网站名
        :return:成功返回Success，失败返回Fail
        """
        if imgurl == '' or source == '':
            return "Fail"
        oldurl = imgurl if imgurl.startswith('http') else "http://" + imgurl
        filename = self.md5(imgurl) + '.jpg'
        newurl = self.getHomeImageUrl(imgurl, source)
        if not newurl=="":
            data = {
                'fileName'  : filename,
                'oldUrl'    : html.unescape(oldurl),  # 对url进行html转义，确保能访问
                'newUrl'    : newurl,
                'sourceName': source,
            }
            json_data = json.dumps(data)
            self.imgRedis.lpush('IMG_ALI_OSS', json_data)
            return "Success"
        else:
            print("图片链接转换失败，可能原因为未将源信息添加入数据库")
            return "Fail"

    def clearText(self, content,author):
        """
        清洗掉一些不需要的东西脚注
        :param context:
        :return: 清洗好的文本
        """
        ptags = re.findall('>([^<]+)<', content)
        count = 0
        while count < 5 if len(ptags) >5 else len(ptags):  # 如果倒数5个句子有脚注行为，删除该文本。
            lasttag = ptags[-1]
            if len(lasttag) < 50 and re.findall('[©|编剧|作者|编辑|版权|侵权|法律|转载|本文|责编]', lasttag):
                content = re.sub(lasttag, '', content)
            ptags.remove(lasttag)
            count = count + 1
        content = re.sub(author, '', content)
        return content

    def replaceImgUrl(self, content, sourceurl,source):
        """
        替换掉文章正文中的图片链接为我们自己的链接
        :param content: 正文html
        :param sourceurl: img链接
        :return: 替换好的正文html
        """
        newimgurl = self.getHomeImageUrl(sourceurl,source)
        content = content.replace(sourceurl, newimgurl)
        return content

    def saveArticle(self, url, title, author, content, status, source, create_time, has_img=0):
        """
        文章图片处理后保存入库
        图片入redis数据库
        :return:
        """
        if not self.hasSpidered(url):
            imgurls = self.getImgUrls(content)
            if imgurls:
                has_img = 1
            for img in imgurls:
                content = self.replaceImgUrl(content, img,source)
                self.saveImage(imgurl=img, source=source)
            content=self.clearText(content,author)
            try:
                self.cursor.execute(
                    '''INSERT INTO spider_posts(url,title,author,content,status,has_img,hash,source,fetch_time,create_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                    (url, title, author, content, status, has_img, self.md5(url), source, int(time.time()), create_time)
                )
                self.conn.commit()
                print('数据插入成功：' + title + url)
                return True
            except Exception as e:
                self.conn.rollback()
                print('数据插入失败：' + title + url)
                print('失败原因：' + str(e))
                return False
        else:
            print("数据已存在：" + title + url)
            return False

    def sendSpiderRequest(self,url,args="",method='get',timeout=7):
        """
        发送爬虫请求（自动添加UA，ip代理等）
        :param url:链接地址
        :param args:请求参数
        :param method:请求方法
        :return:response对象
        """
        resp=""
        for i in range(5):
            try:
                if method=='get':
                    resp = requests.get(url, params=args, headers=self.getHeader(), proxies=self.getProxy(), timeout=timeout)
                elif method == 'post':
                    resp = requests.post(url, data=args,headers=self.getHeader(), proxies=self.getProxy(), timeout=timeout)
                break
            except Exception as e:
                print("爬虫请求失败，重试5次: " + url)
        return resp


if __name__ == '__main__':
    com = spiderTools()
    print(com.getHomeImageUrl("http://34343434.jpg",'百家号'))
