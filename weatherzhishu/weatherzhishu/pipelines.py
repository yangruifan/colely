# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from weatherzhishu.settings import LOCALHOST, USER, PASSWORD, DB, PORT
import time


class WeatherZhishuPipeline(object):
    def __init__(self):
        self.db = pymysql.connect(
            host=LOCALHOST,
            port=PORT,
            user=USER,
            passwd=PASSWORD,
            db=DB,
            charset="utf8",
            use_unicode=True)
        self.cursor = self.db.cursor()
        self.dbname = 'weather_zhishu'

    def process_item(self, item, spider):
        try:
            self.db.ping()
        except:
            self.db = pymysql.connect(
                host=LOCALHOST,
                port=PORT,
                user=USER,
                passwd=PASSWORD,
                db=DB,
                charset="utf8",
                use_unicode=True)
            self.cursor = self.db.cursor()
        sql = "SELECT * FROM {0} WHERE fetch_time='{1}' and countynum='{2}' and num='{3}'".format(self.dbname, item['fetch_time'], item['areanum'], item['num'])
        # 执行sql语句
        self.cursor.execute(sql)
        # time.sleep(1)
        # 获取所有记录列表
        results = self.cursor.fetchall()
        if results == ():
            # SQL插入语句
            sql = ("""
            INSERT INTO {0}(num,name,indexs,details,province,city,county,fetch_time,url,countynum,source)
            VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}')
            """.format(self.dbname, item['num'], item["name"], item["zhishu"], item["zhishu_details"], item["provincename"], item["cityname"], item["areaname"], item["fetch_time"], item["url"], item['areanum'], item['source']))
            # 执行sql语句
            self.cursor.execute(sql)            # 提交到数据库执行
            self.db.commit()
        else:
            print('当天{0}的{1}数据已存在。'.format(item['areaname'], item['name']))

        return item