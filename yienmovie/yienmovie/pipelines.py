# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from yienmovie.settings import LOCALHOST, USER, PASSWORD, DB, PORT
import time


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
        self.dbname = 'Cinemal_from_Company'

    def process_item(self, item, spider):
        if item['sqltype'] == '1':
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
            sql = "SELECT * FROM {0} WHERE CompanyID='{1}' and CinemaID='{2}' and OnlineDate='{3}'".format(self.dbname, item['CompanyID'], item['CinemaID'], item['OnlineDate'])
            # 执行sql语句
            self.cursor.execute(sql)
            # 获取所有记录列表
            results = self.cursor.fetchall()
            if results == ():
                # SQL插入语句
                sql = ("""
                INSERT INTO {0}(Companyname,CompanyID,CinemaID,CinemaName,Province,City,Area,OnlineDate,Screen,ScreenD,ScreenS,Seat,Tel,Creat_time,source)
                VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}')
                """.format(self.dbname, item['Companyname'], item["CompanyID"], item["CinemaID"], item["CinemaName"], item["Province"], item["City"], item["Area"], item["OnlineDate"], item["Screen"], item['ScreenD'], item['ScreenS'], item["Seat"], item["Tel"], item['Creat_time'], item['source']))
                # 执行sql语句
                self.cursor.execute(sql)            # 提交到数据库执行
                self.db.commit()
            else:
                print('{0}的{1}影院数据已存在。'.format(item['Companyname'], item['CinemaName']))

        return item


class Pipelinetwo(object):
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
        self.dbname = 'yien_company_related'

    def process_item(self, item, spider):
        if item['sqltype'] == '2':
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
            sql = "SELECT * FROM {0} WHERE CompanyNameA='{1}' and CompanyNameB='{2}'".format(self.dbname, item['Companyname'], item['CompanyName'])
            # 执行sql语句
            self.cursor.execute(sql)
            # 获取所有记录列表
            results = self.cursor.fetchall()
            if results == ():
                # SQL插入语句
                sql = ("""
                INSERT INTO {0}(CompanyNameA,CompanyIdA,CompanyNameB,CompanyIdB,Num,CompanyType,Creat_time,source)
                VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}')
                """.format(self.dbname, item['Companyname'], item["CompanyID"], item["CompanyName"], item["CompanyId"], item["Num"], item["CompanyType"], item["Creat_time"], item["source"]))
                # 执行sql语句
                self.cursor.execute(sql)            # 提交到数据库执行
                self.db.commit()
            else:
                print('{0}与{1}合作的数据已存在。'.format(item['Companyname'], item['CompanyName']))

        return item