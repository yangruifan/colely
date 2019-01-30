import re
import json
import pymysql
import datetime
import hashlib
from aip import AipNlp
from multiprocessing import Pool
import time

#######<---配置信息--->########################################################
my_sql = {
    'db': 'market_spider',
    'user': 'root',
    'password': 'samVW!$#jh',
    'host': 'gz-cdb-l4r5h3m3.sql.tencentcdb.com',
    'port': 61928
}
my_sql1 = {
    'db': 'dss_movie',
    'user': 'root',
    'password': 'samVW!$#jh',
    'host': 'gz-cdb-dcwhfcdd.sql.tencentcdb.com',
    'port': 61902
}  # 广电
###############################################################################

class move_inverst():
    def __init__(self):
        self.connect_db()
        self.connect_db1()
        self.dbname = 'cinemal_from_company'
        self.dbname1 = 'base_cinema_invest'
        self.dbname2 = 'cinema'

    def get_md5(self, data):
        if isinstance(data, str):
            data = data.encode("utf-8")
        m = hashlib.md5()
        m.update(data)
        return m.hexdigest()

    def connect_db(self):
        self.db = pymysql.connect(
            **my_sql,
            charset="utf8",
            use_unicode=True)
        self.cursor = self.db.cursor()

    def connect_db1(self):
        self.db1 = pymysql.connect(
            **my_sql1,
            charset="utf8",
            use_unicode=True)
        self.cursor1 = self.db1.cursor()

    def move_cinema_invest(self):

        """将数据库中cinemal_from_company表的数据进行不重复查询，然后插入到广电的base_cinema_invest表中"""
        sql = """select distinct Companyname  from {0}""".format(self.dbname)
        # 执行sql语句
        self.cursor.execute(sql)
        # 获取所有记录列表
        results = self.cursor.fetchall()
        for inverst in results:
            inverst_hash = self.get_md5(inverst[0])
            sql = """select * from {0} where code='{1}'""".format(self.dbname1, inverst_hash)
            # 执行sql语句
            self.cursor1.execute(sql)
            # 获取所有记录列表
            datas = self.cursor1.fetchall()
            creat_time = datetime.datetime.now().strftime('%Y-%m-%d')
            if not datas:
                sql = """INSERT INTO %s(REVISION,CREATED_BY,CREATED_TIME,UPDATED_BY,UPDATED_TIME,STATUS,name,code)
                         VALUES (%r,%r,%r,%r,%r,%r,%r,%r) """\
                      % (self.dbname1, '0', 'colely', creat_time, 'colely', creat_time, '1', inverst[0], inverst_hash)
                print("插入%s数据。" % (inverst[0]))
            else:
                sql = """UPDATE %s SET UPDATED_BY=%r,UPDATED_TIME=%r WHERE code=%r
                """ % (self.dbname1, 'colely', creat_time, inverst_hash)
                print("更新%s数据。" % (inverst[0]))
            try:
                self.db1.ping()
            except:
                self.connect_db1()
            # 执行sql语句
            self.cursor1.execute(sql)
            self.db1.commit()

    def get_cinema_name(self):

        sql = """select distinct City,Province from %s""" % self.dbname
        # 执行sql语句
        self.cursor.execute(sql)
        # 获取所有记录列表
        results = self.cursor.fetchall()
        for result in results:
            sql = """select CinemaName,Companyname from %s where City=%r""" % (self.dbname, result[0])
            # 执行sql语句
            self.cursor.execute(sql)
            # 获取所有记录列表
            datas1 = self.cursor.fetchall()
            sql = """select id,shortName from %s where city like %r""" % (self.dbname2, result[0].replace('市', '') + '%')
            # 执行sql语句
            self.cursor1.execute(sql)
            # 获取所有记录列表
            datas2 = self.cursor1.fetchall()
            if not datas2:
                sql = """select id,shortName from %s where province like %r""" % (
                self.dbname2, result[1].replace('省', '') + '%')
                # 执行sql语句
                self.cursor1.execute(sql)
                # 获取所有记录列表
                datas2 = self.cursor1.fetchall()
            else:
                pass
            yield 1
            yield datas1
            # print(datas1)
            yield datas2


def baiduapiconnect():
    """
    文本匹配接口
    """
    APP_ID1 = '11205369'
    API_KEY1 = 'LPss0udLlPZGqrX0PPAaMzVj'
    SECRET_KEY1 = 'nSeWOwVQeeBnTv7LGK6AlTYCdTrUo095 '
    client = AipNlp(APP_ID1, API_KEY1, SECRET_KEY1)
    return client


def cinema_cinema(a, b):
    client = baiduapiconnect()
    score = []
    scoreson = []
    for data2 in b:
        num = client.simnet(a[0], data2[1])
        score.append({'num': num['score'],  # 匹配值
                      'data1': a[0],  # 影投影院
                      'data2': data2[1],  # 影院名称
                      'id': data2[0],  # 影院id
                      'company': a[1],  # 影投公司
                      })
        scoreson.append(num['score'])
        print(a[0], data2[1], num['score'])
    datas = score[scoreson.index(max(scoreson))]

    def connect_db():
        db = pymysql.connect(
            **my_sql1,
            charset="utf8",
            use_unicode=True)
        return db

    db = connect_db()
    cursor = db.cursor()
    sql = """select ID from base_cinema_invest where name=%r
            """ % datas['company']
    cursor.execute(sql)
    # 获取所有记录列表
    companyid = cursor.fetchall()
    sql = """select * from rela_cinema_invest where cinema_id=%r and invest_id=%r
            """ % (datas['id'], companyid[0][0])
    cursor.execute(sql)
    # 获取所有记录列表
    infor = cursor.fetchall()
    if not infor:
        sql = """INSERT INTO rela_cinema_invest(cinema_id,invest_id)
                VALUES (%r,%r) """ % (datas['id'], companyid[0][0])
        cursor.execute(sql)
        db.commit()
    else:
        pass


if __name__ == '__main__':
    pro = move_inverst()
    pro.move_cinema_invest()
    data = pro.get_cinema_name()
    while next(data):
        a = next(data)
        b = next(data)
        p = Pool(100)
        for i in range(len(a)):
            p.apply_async(cinema_cinema, args=(a[i], b,))
            # p.apply_async(long_time_task, args=(a[i],))
        p.close()
        p.join()



