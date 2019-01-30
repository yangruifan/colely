# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from tenxun_news.settings import LOCALHOST, USER, PASSWORD, DB, PORT, DBNAME


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
        self.dbname = DBNAME

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
        sql = "SELECT * FROM {0} WHERE hash='{1}'".format(self.dbname, item['url_hash'])
        # 执行sql语句
        self.cursor.execute(sql)
        # 获取所有记录列表
        results = self.cursor.fetchall()
        if results == ():
            # SQL插入语句
            sql = ("""
            INSERT INTO {0}(url,hash,title,content,has_img,source,create_time,fetch_time)
            VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}')
            """.format(self.dbname, item['url'], item["url_hash"], item["title"], item["content"], item["has_img"], item["source"], item["creat_time"], item["fetch_time"]))
            # 执行sql语句
            self.cursor.execute(sql)            # 提交到数据库执行
            self.db.commit()
        else:
            print('url={0}::《{1}》数据已存在。'.format(item['url'], item['title']))

        return item