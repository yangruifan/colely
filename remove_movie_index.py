# -*- coding: utf-8 -*-
import re
import json
import pymysql
import datetime

# LOCALHOST = "localhost"
# USER = "root"
# PASSWORD = "960823"
# DB = "maizuo"
# PORT = 3306


LOCALHOST = "gz-cdb-l4r5h3m3.sql.tencentcdb.com"
USER = "root"
PASSWORD = "samVW!$#jh"
DB = "market_spider"
PORT = 61928

LOCALHOST1 = "gz-cdb-dcwhfcdd.sql.tencentcdb.com" # 广电
DB1 = "dss_movie" # 广电
PORT1 = 61902 # 广电


class from_movie_index():
    def __init__(self):
        self.dbname = 'movie_index'
        self.dbname1 = 'spider_movie_index'
        self.connect_db()
        self.connect_db1()

    def connect_db(self):
        self.db = pymysql.connect(
            host=LOCALHOST,
            port=PORT,
            user=USER,
            passwd=PASSWORD,
            db=DB,
            charset="utf8",
            use_unicode=True)
        self.cursor = self.db.cursor()

    def connect_db1(self):
        self.db1 = pymysql.connect(
            host=LOCALHOST1,
            port=PORT1,
            user=USER,
            passwd=PASSWORD,
            db=DB1,
            charset="utf8",
            use_unicode=True)
        self.cursor1 = self.db1.cursor()

    def remove_datas(self):
        # 查询指数表中的信息
        startnum = 0
        endnum = 1000
        sql = """select count(*) from {}""".format(self.dbname)
        # 执行sql语句
        self.cursor.execute(sql)
        # 获取所有记录列表
        results = self.cursor.fetchall()
        overnum = results[0][0]
        while True:
            sql = """ SELECT * FROM {0} WHERE stutas=0  limit {start},{end}
            """.format(self.dbname, start=startnum, end=endnum)
            # 执行sql语句
            self.cursor.execute(sql)
            # 获取所有记录列表
            results = self.cursor.fetchall()
            if startnum > overnum:
                break
            else:
                startnum = endnum
                endnum = endnum + 1000
            if results != ():
                for data in results:
                    film_name = data[1]
                    film_code = data[2]
                    avg_all = data[3]
                    if avg_all == '' or avg_all == None:
                        avg_all = 0
                    avg_pc = data[4]
                    if avg_pc == '' or avg_pc == None:
                        avg_pc = 0
                    avg_wise = data[5]
                    if avg_wise == '' or avg_wise == None:
                        avg_wise = 0
                    avg_news = data[6]
                    if avg_news == '' or avg_news == None:
                        avg_news = 0
                    date = data[7]
                    flag = data[8]
                    source = data[9]
                    creat_time = data[11]
                    if creat_time == '' or creat_time == None:
                        creat_time = datetime.datetime.now().strftime('%Y-%m-%d')

                    sql1 = """ SELECT * FROM {0} WHERE flag = {1} """.format(self.dbname1, flag)
                    # 执行sql语句
                    self.cursor1.execute(sql1)
                    # 获取所有记录列表
                    results = self.cursor1.fetchall()
                    if results == ():
                    # SQL插入语句
                        sql2 = """INSERT INTO {0}(film_name,film_code,avg_all,avg_pc,avg_wise,avg_news,avg_date,flag,source,CREATED_TIME)
                    VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}')""".format(self.dbname1, film_name, film_code, avg_all, avg_pc, avg_wise, avg_news, date, flag, source, creat_time)
                        # print(sql2)
                        self.cursor1.execute(sql2)  # 提交到数据库执行
                        self.db1.commit()
                        print('<------------------------------------------------------------------------------------------------------------------------------------------------------------>')
                        print(data, "：插入成功。")
                        sql = "UPDATE {0} SET stutas='{1}' WHERE flag='{2}'".format(self.dbname, 1, flag)
                        self.cursor.execute(sql)  # 提交到数据库执行
                        self.db.commit()
                    else:
                        print('<------------------------------------------------------------------------------------------------------------------------------------------------------------>')
                        print(data, "：数据存在。")
                        sql = "UPDATE {0} SET stutas='{1}' WHERE flag='{2}'".format(self.dbname, 1, flag)
                        self.cursor.execute(sql)  # 提交到数据库执行
                        self.db.commit()


class from_movie_related():
    def __init__(self):
        self.dbname = 'movieindex_about_related'
        self.dbname1 = 'spider_movie_word_relate'
        self.connect_db()
        self.connect_db1()

    def connect_db(self):
        self.db = pymysql.connect(
            host=LOCALHOST,
            port=PORT,
            user=USER,
            passwd=PASSWORD,
            db=DB,
            charset="utf8",
            use_unicode=True)
        self.cursor = self.db.cursor()

    def connect_db1(self):
        self.db1 = pymysql.connect(
            host=LOCALHOST1,
            port=PORT1,
            user=USER,
            passwd=PASSWORD,
            db=DB1,
            charset="utf8",
            use_unicode=True)
        self.cursor1 = self.db1.cursor()

    def remove_datas_first(self):
        startnum = 0
        endnum = 1000
        sql = """select count(*) from {}""".format(self.dbname)
        # 执行sql语句
        self.cursor.execute(sql)
        # 获取所有记录列表
        results = self.cursor.fetchall()
        overnum = results[0][0]
        while True:
            sql = """ SELECT * FROM {0} WHERE stutas=0  limit {start},{end}
                        """.format(self.dbname, start=startnum, end=endnum)
            # 执行sql语句
            self.cursor.execute(sql)
            # 获取所有记录列表
            results = self.cursor.fetchall()
            if startnum > overnum:
                break
            else:
                startnum = endnum
                endnum = endnum + 1000
            if results != ():
                for data in results:
                    film_name = data[1]
                    film_code = data[2]
                    statistics_date = data[3][0:4] + '-' + data[3][4:6] + '-' + data[3][6:8]
                    source = data[11]
                    if source == '百度指数':
                        source = 1
                    link_name = data[5]
                    one = data[6]
                    two = data[7]
                    three = data[8]
                    four = data[9]
                    five = data[10]
                    CREATED_TIME = data[4]
                    sql1 = """ SELECT * FROM {0} WHERE link_name='{1}' and statistics_date='{2}' """.format(self.dbname1, link_name, statistics_date)
                    # 执行sql语句
                    self.cursor1.execute(sql1)
                    # 获取所有记录列表
                    results = self.cursor1.fetchall()
                    if results == ():
                        sql2 = """INSERT INTO {0}(film_name,film_code,statistics_date,source,link_name,one,two,three,four,five,CREATED_TIME)
                                            VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}')""".format(
                            self.dbname1, film_name, film_code, statistics_date, source, link_name, one, two, three, four, five, CREATED_TIME)
                        # print(sql2)
                        self.cursor1.execute(sql2)  # 提交到数据库执行
                        self.db1.commit()
                        print('<------------------------------------------------------------------------------------------------------------------------------------------------------------>')
                        print(data, "：插入成功。")
                        sql = "UPDATE {0} SET stutas='{1}' WHERE link_name='{2}' and date='{3}'".format(self.dbname, 1, link_name, data[3])
                        self.cursor.execute(sql)  # 提交到数据库执行
                        self.db.commit()
                    else:
                        sql = "UPDATE {0} SET stutas='{1}' WHERE link_name='{2}' and date='{3}'".format(self.dbname, 1, link_name, data[3])
                        self.cursor.execute(sql)  # 提交到数据库执行
                        self.db.commit()
                        print('<------------------------------------------------------------------------------------------------------------------------------------------------------------>')
                        print(data, "：数据存在。")

    def find_film_id(self):
        try:
            self.db1.ping()
        except:
            self.connect_db1()
        sql = """SELECT distinct film_name FROM {} where STATUS=0""".format(self.dbname1)
        # 执行sql语句
        self.cursor1.execute(sql)
        # 获取所有记录列表
        results = self.cursor1.fetchall()
        if results != ():
            for film_name in results:
                sql = """select id from film where name='{0}'""".format(film_name[0])
                # 执行sql语句
                self.cursor1.execute(sql)
                results = self.cursor1.fetchall()
                if results != ():
                    sql = "UPDATE {0} SET film_id='{1}',STATUS=1 WHERE film_name='{2}'".format(self.dbname1, results[0][0], film_name[0])
                    self.cursor1.execute(sql)  # 提交到数据库执行
                    self.db1.commit()
                else:
                    print('<------------------------------------------------------------------------------------------------------------------------------------------------------------>')
                    print("{}的ID不存在dss.movie->film表中".format(film_name[0]))


class from_movieindex_about_region():
    def __init__(self):
        self.dbname = 'movieindex_about_region'
        self.dbname1 = 'spider_movie_region_index'
        self.connect_db()
        self.connect_db1()

    def connect_db(self):
        self.db = pymysql.connect(
            host=LOCALHOST,
            port=PORT,
            user=USER,
            passwd=PASSWORD,
            db=DB,
            charset="utf8",
            use_unicode=True)
        self.cursor = self.db.cursor()

    def connect_db1(self):
        self.db1 = pymysql.connect(
            host=LOCALHOST1,
            port=PORT1,
            user=USER,
            passwd=PASSWORD,
            db=DB1,
            charset="utf8",
            use_unicode=True)
        self.cursor1 = self.db1.cursor()

    def remove_data_first(self):
        startnum = 0
        endnum = 1000
        sql = """select count(*) from {}""".format(self.dbname)
        # 执行sql语句
        try:
            self.db.ping()
        except:
            self.connect_db()
        self.cursor.execute(sql)
        # 获取所有记录列表
        results = self.cursor.fetchall()
        overnum = results[0][0]
        while True:
            sql = """ SELECT * FROM {0} WHERE stutas=0  limit {start},{end}
                        """.format(self.dbname, start=startnum, end=endnum)
            try:
                self.db.ping()
            except:
                self.connect_db()
            # 执行sql语句
            self.cursor.execute(sql)
            # 获取所有记录列表
            results = self.cursor.fetchall()
            if startnum > overnum:
                break
            else:
                startnum = endnum
                endnum = endnum + 1000
            if results != ():
                for data in results:
                    film_name = data[1]
                    film_code = data[2]
                    city_name = data[3]
                    hot_value = data[5]
                    num = data[6].index('|')
                    creat_time = data[6][0:num]
                    fetch_time = data[7]
                    province = data[8]
                    if province == '全国':
                        province = city_name
                    source = data[9]
                    if source == '百度指数':
                        source = 1
                    sql1 = """ SELECT * FROM {0} WHERE film_name='{1}' and city='{2}' and statistics_date='{3}' """.format(
                        self.dbname1, film_name, city_name, creat_time)
                    try:
                        self.db1.ping()
                    except:
                        self.connect_db1()
                    # 执行sql语句
                    self.cursor1.execute(sql1)
                    # 获取所有记录列表
                    results = self.cursor1.fetchall()
                    if results == ():
                        sql2 = """INSERT INTO {0}(film_name,film_code,statistics_date,source,hot_value,province,city,CREATED_TIME)
                                  VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}')""".format(
                            self.dbname1, film_name, film_code, creat_time, source, hot_value, province, city_name, fetch_time)
                        # print(sql2)
                        try:
                            self.db1.ping()
                        except:
                            self.connect_db1()
                        self.cursor1.execute(sql2)  # 提交到数据库执行
                        self.db1.commit()
                        print('<------------------------------------------------------------------------------------------------------------------------------------------------------------>')
                        print(data, "：插入成功。")
                        sql = "UPDATE {0} SET stutas='{1}' WHERE movie='{2}' and date='{3}' and region='{4}'".format(self.dbname, 1, film_name, data[6], city_name)
                        try:
                            self.db.ping()
                        except:
                            self.connect_db()
                        self.cursor.execute(sql)  # 提交到数据库执行
                        self.db.commit()
                    else:
                        print('<------------------------------------------------------------------------------------------------------------------------------------------------------------>')
                        print(data, "：数据存在。")
                        try:
                            self.db.ping()
                        except:
                            self.connect_db()
                        sql = "UPDATE {0} SET stutas='{1}' WHERE movie='{2}' and date='{3}' and region='{4}'".format(self.dbname, 1, film_name, data[6], city_name)
                        self.cursor.execute(sql)  # 提交到数据库执行
                        self.db.commit()

    def find_film_id(self):
        try:
            self.db1.ping()
        except:
            self.connect_db1()
        # select distinct film_name from spider_movie_region_index where
        sql = """SELECT distinct film_name FROM {} where film_id is null""".format(self.dbname1)
        # 执行sql语句
        self.cursor1.execute(sql)
        # 获取所有记录列表
        results = self.cursor1.fetchall()
        if results != ():
            for film_name in results:
                sql = """select id from film where name='{0}'""".format(film_name[0])

                try:
                    self.db1.ping()
                except:
                    self.connect_db1()
                # 执行sql语句
                self.cursor1.execute(sql)
                results = self.cursor1.fetchall()
                if results != ():
                    sql = "UPDATE {0} SET film_id='{1}' WHERE film_name='{2}'".format(self.dbname1, results[0][0], film_name[0])
                    self.cursor1.execute(sql)  # 提交到数据库执行
                    self.db1.commit()
                    print('<------------------------------------------------------------------------------------------------------------------------------------------------------------>')
                    print("{}的ID填充完成。".format(film_name[0]))
                else:
                    print('<------------------------------------------------------------------------------------------------------------------------------------------------------------>')
                    print("{}的ID不存在dss.movie->film表中".format(film_name[0]))

    def find_province_id(self):
        try:
            self.db1.ping()
        except:
            self.connect_db1()
            # select distinct film_name from spider_movie_region_index where
        sql = """SELECT distinct province FROM {} where province_id is null""".format(self.dbname1)
        # 执行sql语句
        self.cursor1.execute(sql)
        # 获取所有记录列表
        results = self.cursor1.fetchall()
        if results != ():
            for province in results:
                sql = """select ID from base_region where NAME like '%{0}%' and STATUS=1""".format(province[0])
                try:
                    self.db1.ping()
                except:
                    self.connect_db1()
                # 执行sql语句
                self.cursor1.execute(sql)
                results = self.cursor1.fetchall()
                if results != ():
                    sql = "UPDATE {0} SET province_id='{1}' WHERE province='{2}'".format(self.dbname1, results[0][0], province[0])
                    self.cursor1.execute(sql)  # 提交到数据库执行
                    self.db1.commit()
                    print('<------------------------------------------------------------------------------------------------------------------------------------------------------------>')
                    print("{}省的ID填充完成。".format(province[0]))
                else:
                    print('<------------------------------------------------------------------------------------------------------------------------------------------------------------>')
                    print("{}省的ID不存在dss.movie->base_region表中".format(province[0]))

    def find_city_id(self):
        try:
            self.db1.ping()
        except:
            self.connect_db1()
            # select distinct film_name from spider_movie_region_index where
        sql = """SELECT distinct city FROM {} where city_id is null""".format(self.dbname1)
        # 执行sql语句
        self.cursor1.execute(sql)
        # 获取所有记录列表
        results = self.cursor1.fetchall()
        if results != ():
            for city_name in results:
                sql = """select ID from base_region where NAME like '%{0}%' and STATUS=1""".format(city_name[0])
                try:
                    self.db1.ping()
                except:
                    self.connect_db1()
                # 执行sql语句
                self.cursor1.execute(sql)
                results = self.cursor1.fetchall()
                if results != ():
                    sql = "UPDATE {0} SET city_id='{1}',STATUS=1 WHERE city='{2}'".format(self.dbname1, results[0][0], city_name[0])
                    self.cursor1.execute(sql)  # 提交到数据库执行
                    self.db1.commit()
                    print('<------------------------------------------------------------------------------------------------------------------------------------------------------------>')
                    print("{}市的ID填充完成。".format(city_name[0]))
                else:
                    print('<------------------------------------------------------------------------------------------------------------------------------------------------------------>')
                    print("{}市的ID不存在dss.movie->base_region表中".format(city_name[0]))


# <代码调用------------------------------------------------------------------------------------------->
def spider_film_index():
    """
    连接数据库，调用数据转移模块。
    """
    data = from_movie_index()
    data.remove_datas()


def spider_movie_word_relate():
    """
    连接数据库，调用部分数据转移模块，查询电影id。
    """
    data = from_movie_related()
    data.remove_datas_first()
    data.find_film_id()


def spider_movie_region_index():
    """
    连接数据库，调用部分数据转移模块，查询电影id,查询省份id，查询城市id。
    """
    data = from_movieindex_about_region()
    data.remove_data_first()
    data.find_province_id()
    data.find_city_id()
    data.find_film_id()


if __name__ == '__main__':
    spider_film_index()
    spider_movie_word_relate()
    spider_movie_region_index()

