# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from sougou_spider.settings import LOCALHOST, USER, PASSWORD, DB, PORT


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
        self.dbname = 'movie_index'

    def process_item(self, item, spider):

        sql = "SELECT * FROM {0} WHERE source='{1}' and film_name='{2}' and avg_date='{3}'".format(self.dbname, item['source'], item['name'], item['create_time'])
        # 执行sql语句
        self.cursor.execute(sql)
        # 获取所有记录列表
        results = self.cursor.fetchall()
        if results == ():
            if item['sql_flag'] == '1':
                #SQL插入语句
                sql = """
                INSERT INTO {}(film_name,film_code,avg_all,avg_date,source,CREATED_TIME,flag)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
                """.format(self.dbname)
                # 执行sql语句
                self.cursor.execute(sql, (
                item["name"], item["name_hash"], item["allavg"], item["create_time"], item["source"], item["fetch_time"], item['flag']))
                # 提交到数据库执行
                self.db.commit()
            else:
                #SQL插入语句
                sql = """
                INSERT INTO {}(film_name,film_code,avg_wise,avg_date,source,CREATED_TIME)
                VALUES (%s,%s,%s,%s,%s,%s)
                """.format(self.dbname)
                # 执行sql语句
                self.cursor.execute(sql, (
                item["name"], item["name_hash"], item["wiseavg"], item["create_time"], item["source"], item["fetch_time"]))
                # 提交到数据库执行
                self.db.commit()
        else:
            if item["sql_flag"] == '1':
                # sql更新语句
                sql = "UPDATE {0} SET avg_all='{1}' WHERE source='{2}' and film_name='{3}' and avg_date='{4}'".format(
                    self.dbname, item["allavg"], item['source'], item['name'], item['create_time'])
            else:
                # sql更新语句
                sql = "UPDATE {0} SET avg_wise='{1}' WHERE source='{2}' and film_name='{3}' and avg_date='{4}'".format(
                    self.dbname, item["wiseavg"], item['source'], item['name'], item['create_time'])
            # 执行SQL语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
        return item


    def MySQL_close(self):
        self.cursor.close()