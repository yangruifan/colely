# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from xiaofeishuiping.settings import LOCALHOST, USER, PASSWORD, DB, PORT
import time


class ZhishuPipeline(object):
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
        self.dbname = 'expense_index'

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
        sql = "SELECT * FROM {0} WHERE name_code='{1}' and city_code='{2}' and creat_time='{3}'".format(self.dbname, item['name_code'], item['city_code'], item['creat_time'])
        # 执行sql语句
        self.cursor.execute(sql)
        # time.sleep(1)
        # 获取所有记录列表
        results = self.cursor.fetchall()
        if results == ():
            # SQL插入语句
            sql = ("""
            INSERT INTO {0}(name,name_code,city,city_code,indexs,creat_time,fetch_time,source)
            VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}')
            """.format(self.dbname, item['name'], item["name_code"], item["city"], item["city_code"], item["indexs"], item["creat_time"], item["fetch_time"], item['source']))
            # 执行sql语句
            self.cursor.execute(sql)            # 提交到数据库执行
            self.db.commit()
        else:
            print('{0}--{1}--{2}--数据已存在。'.format(item['creat_time'], item['city'], item['name']))

        return item