# -*- coding: utf-8 -*-
import pymysql
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
mysql = {
    'host': 'localhost',
    'port': 3306,
    'db': 'scrapy',
    'user': 'root',
    'password': '960823',
}


class FangtianxiaPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(
            **mysql,
            charset='utf8',
            use_unicode=True
        )
        self.cursor = self.conn.cursor()
        self.dbname = 'fangtianxia'

    def process_item(self, item, spider):
        try:
            self.conn.ping()
        except:
            self.conn = pymysql.connect(
                **mysql,
                charset='utf8',
                use_unicode=True
            )
            self.cursor = self.conn.cursor()
        sql = """select * from %s WHERE url_hash= %r""" % (self.dbname, item['url_hash'])
        # 执行SQL语句
        self.cursor.execute(sql)
        # 获取所有记录列表
        results = self.cursor.fetchall()
        if not results:
            sql = """INSERT INTO %s(url,url_hash,title,city,oldprice,nowprice,xiaoqudizhi,lvhualv,wuyegongsi,jianzhujiegou,rongjilv,youbian,loudong,wuyefei,jianzhuniandai,kaifashang,jianzhumianji,fangwuzongshu,wuyeleibie,fujiaxinxi,zhandimianji,jianzhuleixing,chanquanmiansu,suoshuquyu)
                      VALUES (%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r)""" % (self.dbname, item['url'], item['url_hash'], item['title'], item['city'], item['oldprice'], item['nowprice'], item['xiaoqudizhi'], item['lvhualv'], item['wuyegongsi'], item['jianzhujiegou'], item['rongjilv'], item['youbian'], item['loudong'], item['wuyefei'], item['jianzhuniandai'], item['kaifashang'], item['jianzhumianji'], item['fangwuzongshu'], item['wuyeleibie'], item['fujiaxinxi'], item['zhandimianji'], item['jianzhuleixing'], item['chanquanmiansu'], item['suoshuquyu'])
            # 执行SQL语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.conn.commit()
        return item
