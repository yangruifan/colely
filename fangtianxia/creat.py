import pymysql

# 创建mysql表
def ceartTable(cursor):
    # # 创建students 数据库, 如果存在则删除students 数据库
    # cursor.execute("drop database if exists scrapy")
    # cursor.execute("create database scrapy")

    # 选择 students 这个数据库
    cursor.execute("use scrapy")

    # sql中的内容为创建一个名为student的表
    sql = """CREATE TABLE IF NOT EXISTS `fangtianxia` (
              
            `url` VARCHAR(200),
            `url_hash` varchar(32),
            `oldprice` varchar(20),
            `nowprice` varchar(20),
            `xiaoqudizhi` varchar(100),
            `lvhualv` varchar(10),
            `wuyegongsi` varchar(30),
            `jianzhujiegou` varchar(32),
            `rongjilv` varchar(10),
            `youbian` varchar(7),
            `loudong` varchar(10),
            `wuyefei` varchar(30),
            `jianzhuniandai` varchar(30),
            `kaifashang` varchar(50),
            `jianzhumianji` varchar(32),
            `fangwuzongshu` varchar(32),
            `wuyeleibie` varchar(32),
            `fujiaxinxi` varchar(32),
            `zhandimianji` varchar(32),
            `jianzhuleixing` varchar(32),
            `chanquanmiansu` varchar(50),
            `suoshuquyu` varchar(50),
             PRIMARY KEY( url_hash )
              )"""
    # 如果存在student这个表则删除
    cursor.execute("drop table if exists fangtianxia")
    # 创建表
    cursor.execute(sql)

    print("successfully create table")
if __name__ == '__main__':
    # 链接mysql数据库
    db = pymysql.connect("localhost", "root", "960823", charset="utf8")
    # 创建指针
    cursor = db.cursor()

    # 创建数据库和表
    ceartTable(cursor)


    # 关闭游标链接
    cursor.close()
    # 关闭数据库服务器连接，释放内存
    db.close()