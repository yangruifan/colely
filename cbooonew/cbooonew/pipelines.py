# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from cbooonew.settings import LOCALHOST, USER, PASSWORD, DB, PORT



class Pipeline(object):
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
        self.dbname = 'cbooo_movie_event'
        self.dbname1 = 'cbooo_event'

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
        sql = "SELECT * FROM {0} WHERE event='{1}'".format(self.dbname1, item['event'])
        # 执行sql语句
        self.cursor.execute(sql)
        # 获取所有记录列表
        results = self.cursor.fetchall()
        if results == ():
            # SQL插入语句
            sql = ("""
            INSERT INTO {0}(event)
            VALUES ('{1}')
            """.format(self.dbname1, item['event']))
            # 执行sql语句
            self.cursor.execute(sql)            # 提交到数据库执行
            self.db.commit()
        else:
            print('{}事件类型已存在。'.format(item['event']))

        sql = "SELECT * FROM {0} WHERE title='{1}' and creat_time='{2}'".format(self.dbname, item['title'], item['creat_time'])
        # 执行sql语句
        self.cursor.execute(sql)
        # 获取所有记录列表
        results = self.cursor.fetchall()
        if results == ():
            # SQL插入语句
            sql = ("""
            INSERT INTO {0}(movie,movie_hash,event,title,creat_time,page_source,url,url_hash,fetch_time,source)
            VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}')
            """.format(self.dbname, item['movie'], item['movie_hash'], item['event'], item['title'], item['creat_time'], item['page_source'], item['url'], item['url_hash'], item['fetch_time'], item['source']))
            # 执行sql语句
            self.cursor.execute(sql)  # 提交到数据库执行
            self.db.commit()
        return item

