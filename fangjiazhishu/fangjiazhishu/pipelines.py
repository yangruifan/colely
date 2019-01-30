# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from fangjiazhishu.settings import LOCALHOST, USER, PASSWORD, DB, PORT


class FangjiaZhishuPipeline(object):
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
        self.dbname = 'fangjiazhishu'

    def process_item(self, item, spider):
        sql = "SELECT * FROM {0} WHERE fetch_time='{1}' and city='{2}'".format(self.dbname, item['fetch_time'], item['cityname'])
        # 执行sql语句
        self.cursor.execute(sql)
        # 获取所有记录列表
        results = self.cursor.fetchall()
        if results == ():
            # SQL插入语句
            sql = ("""
            INSERT INTO {0}(city,city_hash,indexs,fetch_time,url,creat_time,source)
            VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}')
            """.format(self.dbname, item['cityname'], item["cityname_hash"], item["num"], item["fetch_time"], item["url"], item['creat_time'], item['source'] ))
            # 执行sql语句
            self.cursor.execute(sql)            # 提交到数据库执行
            self.db.commit()
        else:
            pass

        return item