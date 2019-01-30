# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from wangyidingyue.settings import LOCALHOST, USER, PASSWOED, DB, PORT, DBNAME


class PagePipeline(object):
    def __init__(self):
        self.db = pymysql.connect(
            host=LOCALHOST,
            port=PORT,
            user=USER,
            passwd=PASSWOED,
            db=DB,
            charset="utf8",
            use_unicode=True)
        self.cursor = self.db.cursor()
        self.dbname = DBNAME

    def process_item(self, item, spider):
        # SQL 查询语句
        sql = "SELECT * FROM {0} WHERE hash = '{1}'".format(self.dbname, item['url_hash'])
        # 执行SQL语句
        self.cursor.execute(sql)
        # 获取所有记录列表
        results = self.cursor.fetchall()
        if results == ():
            # SQL 插入语句
            sql = """
            INSERT INTO {}(url,title,author,content,hash,like_num,source,create_time,fetch_time,has_img)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """.format(self.dbname)
            # 执行sql语句
            self.cursor.execute(sql, (item["url"], item["title"], item["author"], item["content"], item["url_hash"], item["like_num"], item["topic"], item["creat_time"], item["fetch_time"], item["has_img"]))
            # 提交到数据库执行
            self.db.commit()
        else:
            pass
        return item

