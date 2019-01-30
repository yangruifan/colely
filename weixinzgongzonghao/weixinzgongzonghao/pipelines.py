# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class BaijiahaoPipeline(object):
    def __init__(self):
        self.db = pymysql.connect("localhost", "root", "960823", "scrapy", charset="utf8", use_unicode=True)
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        # SQL 插入语句
        sql = """
           INSERT INTO baijiahao(name,tittle,tittle_hash,author,author_desc,source,creat_time,spider_time,content,url)
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
           """
        # 执行sql语句
        self.cursor.execute(sql, (
        item["name"], item["tittle"], item["tittle_hash"], item["author"], item["author_desc"],
        item["source"], item["create_time"], item["spider_time"], item["content"], item["url"]))
        # 提交到数据库执行
        self.db.commit()
        return item