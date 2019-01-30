# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from spider_list.Operate_datebase_table import Operate_datebase_table

class DataPipeline(object):
    def __init__(self):
        #连接数据库
        self.db = Operate_datebase_table("spider_posts")

    def process_item(self, item, spider):
        if spider.name == "spider_page":
           self.db.insertTable("(url,title,content,link_id)", ((item["url"],item["title"],item["content"],item["source_id"]),))
        else:
            pass
        return item


class Data_of_pagelistPipeline(object):
    def __init__(self):
        #连接数据库
        self.db = Operate_datebase_table("adv_spider_article_link")

    def process_item(self, item, spider):
        if spider.name == "spider_pageurl":
            self.db.insertTable("(fetched,url,creat_time,source_id)",((item["flag"],item["url"],item["creat_time"],item["source_id"]),))
        else:
            pass
        return item

class SpiderPipeline(object):
    def __init__(self):
        #连接数据库
        self.db = Operate_datebase_table("adv_spider_list_link")
    def process_item(self, item, spider):
        if spider.name == "spider":
            self.db.insertTable("(fetched,url,source_id)",((item["flag"],item["url"],item["source_id"]),))
        else:
            pass
        return item