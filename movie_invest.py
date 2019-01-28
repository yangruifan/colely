import pymysql


#######<---配置信息--->########################################################
my_sql = {
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
        self.dbname = 'rela_cinema_invest'
        self.dbname1 = 'base_cinema_invest'
        self.dbname2 = 'report_cinema'

    def connect_db(self):
        self.db = pymysql.connect(
            **my_sql,
            charset="utf8",
            use_unicode=True)
        self.cursor = self.db.cursor()

    def get_inverst_name(self, id):
        sql = """select name from %s where ID=%r""" % (self.dbname1, id)
        # 执行sql语句
        self.cursor.execute(sql)
        # 获取所有记录列表
        results = self.cursor.fetchall()
        try:
            return results[0][0]
        except IndexError:
            return ''

    def updata_into_report_cinema(self, cinema_id, inverst_id, inverst_name):
        try:
            sql ="""UPDATE %s SET invest_id = %r, invest_name = %r WHERE cinema_id = %r""" % (self.dbname2, inverst_id, inverst_name, cinema_id)
            try:
                self.db.ping()
            except:
                self.connect_db()
            # 执行sql语句
            self.cursor.execute(sql)
            self.db.commit()
            return 0
        except:
            return -1

    def get_inverst(self):
        sql = """select * from %s """ % self.dbname
        # 执行sql语句
        self.cursor.execute(sql)
        # 获取所有记录列表
        results = self.cursor.fetchall()
        for inverst in results:
            cinema_id = inverst[1]
            inverst_id = inverst[2]
            inverst_name = self.get_inverst_name(inverst_id)
            if inverst_name:
                num = self.updata_into_report_cinema(cinema_id, inverst_id, inverst_name)
                if num == 0:
                    print("插入%s影投 %s 成功。" % (cinema_id, inverst_name))
            else:
                pass

    def sql_close(self):
        self.db.close()


if __name__ == '__main__':
    data = move_inverst()
    data.get_inverst()
    data.sql_close()
