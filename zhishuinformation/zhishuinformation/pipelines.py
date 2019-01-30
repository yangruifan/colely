# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from zhishuinformation.settings import LOCALHOST, USER, PASSWORD, DB, PORT


class DianyingzhishuPipeline(object):
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
        if item["sql_flag"] == '1' or item["sql_flag"] == '2':
            # SQL 查询语句
            sql = "SELECT * FROM {0} WHERE flag = '{1}' and film_name = '{2}'".format(self.dbname, item['flag'], item["name"])
            # 执行SQL语句
            self.cursor.execute(sql)
            # 获取所有记录列表
            results = self.cursor.fetchall()
            if results == ():
                if item["sql_flag"] == '1':
                    # SQL 插入语句
                    sql = """
                    INSERT INTO {}(film_name,film_code,avg_all,avg_pc,avg_wise,avg_date,flag,source)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                    """.format(self.dbname)
                    # 执行sql语句
                    self.cursor.execute(sql, (
                    item["name"], item["name_hash"], item["allavg"], item["pcavg"], item["wiseavg"],
                    item["date"], item["flag"], item['source']))
                    # 提交到数据库执行
                    self.db.commit()
                elif item["sql_flag"] == '2':
                    # SQL 插入语句
                    sql = """
                    INSERT INTO {}(film_name,film_code,avg_news,flag)
                    VALUES (%s,%s,%s,%s)
                    """.format(self.dbname)
                    # 执行sql语句
                    self.cursor.execute(sql, (
                        item["name"], item["name_hash"], item["avg"], item["flag"]))
                    # 提交到数据库执行
                    self.db.commit()
                else:
                    pass
            else:
                if item["sql_flag"] == '1':
                    # sql更新语句
                    sql = "UPDATE {0} SET avg_all='{1}',avg_pc='{2}',avg_wise='{3}',avg_date='{4}' WHERE flag='{5}' and film_name='{6}'".format(self.dbname, item["allavg"], item["pcavg"], item["wiseavg"],
                    item["date"], item["flag"], item['name'])
                elif item["sql_flag"] == '2':
                    # sql更新语句
                    sql = "UPDATE {0} SET avg_news='{1}' WHERE flag='{2}' and film_name='{3}'".format(
                        self.dbname, item["avg"], item["flag"], item['name'])
                else:
                    pass
                # 执行SQL语句
                self.cursor.execute(sql)
                # 提交到数据库执行
                self.db.commit()
        else:
            if item["sql_flag"] == '6':
                # SQL 查询语句
                sql = "SELECT * FROM {0} WHERE date = '{1}' and movie = '{2}'".format('movieindex_about_gender', item['date'], item['name'])
                # 执行SQL语句
                self.cursor.execute(sql)
                # 获取所有记录列表
                results = self.cursor.fetchall()
                if results == ():
                    # SQL 插入语句
                    sql = """
                    INSERT INTO {}(movie,movie_hash,date,before_nineteen,twenty_to_thirty,thirty_to_forty,forty_to_fifty,aften_fifty,men,women,source)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""".format('movieindex_about_gender')
                    # 执行sql语句
                    self.cursor.execute(sql, (
                        item["name"], item["name_hash"], item["date"], item["before_nineteen"],
                        item["twenty_to_thirty"],
                        item["thirty_to_forty"], item["forty_to_fifty"], item["aften_fifty"], item["men"],
                        item["women"], item['source']))
                    # 提交到数据库执行
                    self.db.commit()
                else:
                    pass
            elif item["sql_flag"] == '5':
                # SQL 查询语句
                sql = "SELECT * FROM {0} WHERE statistics_date = '{1}' and link_name = '{2}'".format('spider_movie_word_relate', item['date'], item['link_name'])
                # 执行SQL语句
                self.cursor.execute(sql)
                # 获取所有记录列表
                results = self.cursor.fetchall()
                if results == ():
                    # SQL 插入语句
                    sql = """
                    INSERT INTO {}(film_name,film_code,statistics_date,CREATED_TIME,link_name,one,two,three,four,five,source)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""".format('spider_movie_word_relate')
                    # 执行sql语句
                    self.cursor.execute(sql, (
                        item["name"], item["name_hash"], item["date"], item["run_time"], item["link_name"],
                        item["No0"], item["No1"], item["No2"], item["No3"], item["No4"], item['source']))
                    # 提交到数据库执行
                    self.db.commit()
                else:
                    pass
            elif item["sql_flag"] == '3':
                # SQL 查询语句
                sql = "SELECT * FROM {0} WHERE date = '{1}' and region = '{2}' and movie = '{3}'".format('movieindex_about_region', item['date'], item['region'], item['movie'])
                # 执行SQL语句
                self.cursor.execute(sql)
                # 获取所有记录列表
                results = self.cursor.fetchall()
                if results == ():
                    # SQL 插入语句
                    sql = """
                    INSERT INTO {}(movie,movie_hash,date,fetch_time,region,regionnum,indexs,billboard,source)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""".format('movieindex_about_region')
                    # 执行sql语句
                    self.cursor.execute(sql, (
                        item["movie"], item["movie_hash"], item["date"], item["fetch_time"], item["region"],
                        item["regionnum"], item["indexs"], item["billboard"], item["source"]))
                    # 提交到数据库执行
                    self.db.commit()
                else:
                    pass

        return item



