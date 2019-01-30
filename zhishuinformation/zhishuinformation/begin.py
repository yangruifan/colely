import subprocess
import time
import pymysql
import datetime
TIME = 5  # 程序状态检测间隔（单位：秒）
CMD = "app.py"  # 需要执行程序的绝对路径，支持jar 如：D:\\calc.exe 或者D:\\test.jar
LOCALHOST = "gz-cdb-dcwhfcdd.sql.tencentcdb.com"
USER = "root"
PASSWORD = "samVW!$#jh"
DB = "dss_movie"
PORT = 61902

class Auto_Run():
    def __init__(self, sleep_time, cmd):
        self.sleep_time = sleep_time
        self.cmd = cmd
        self.p = None  # self.p为subprocess.Popen()的返回值，初始化为None
        self.db = pymysql.connect(
            host=LOCALHOST,
            port=PORT,
            user=USER,
            passwd=PASSWORD,
            db=DB,
            charset="utf8",
            use_unicode=True)
        self.cursor = self.db.cursor()
        self.dbname = 'movie'
        sql = 'select distinct name from {0} where DATE_SUB(CURDATE(), INTERVAL 1 MONTH) <= date(showDate)'.format(self.dbname,)
        # 执行SQL语句
        self.cursor.execute(sql)
        # 获取所有记录列表
        self.results = self.cursor.fetchall()
        try:
            for word in self.results:
                self.run(word[0])
                self.poll = self.p.poll()
                while self.poll is None:
                    print("运行正常")
                    self.endtime = time.time()
                    if self.endtime-self.starttime > 300:
                        self.p.kill()
                    time.sleep(sleep_time)  # 休息10秒，判断程序状态
                    self.poll = self.p.poll()  # 判断程序进程是否存在，None：表示程序正在运行 其他值：表示程序已退出
                print("未检测到程序运行状态，准备启动程序")

        except KeyboardInterrupt as e:
            print("检测到CTRL+C，准备退出程序!")

    def run(self, word):
        print('start OK!')
        self.starttime = time.time()
        self.p = subprocess.Popen("python {0} {1}".format(self.cmd, word))



app = Auto_Run(TIME, CMD)
