# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from Baidufengyunbangzhishu.settings import LOCALHOST, USER, PASSWOED, DB, PORT


class DianyingzhishuPipeline(object):
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

    def process_item(self, item, spider):
        # SQL 插入语句
        sql = """
        INSERT INTO movie_zhishu(topic_parent,topic,name,name_hash,num,type,create_time)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """
        # 执行sql语句
        self.cursor.execute(sql, (item["class_type_top1"], item["class_type_top2"],item["name"],item["name_hash"],item["baidu_number"],item["type"],item["create_time"]))
        # 提交到数据库执行
        self.db.commit()
        return item

