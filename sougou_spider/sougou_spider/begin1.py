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
        now = datetime.datetime.now()
        delta = datetime.timedelta(days=-30)
        n_days = now + delta
        startday = n_days.strftime('%Y-%m-%d')
        n_days = n_days + delta
        endday = n_days.strftime('%Y-%m-%d')
        while 1:
            if startday > '1949-01-30':
                sql = """SELECT distinct name FROM {0} WHERE showDate < '{1}' AND showDate > '{2}'""".format(self.dbname, startday, endday)
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
                            time.sleep(sleep_time)  # 休息10秒，判断程序状态
                            self.poll = self.p.poll()  # 判断程序进程是否存在，None：表示程序正在运行 其他值：表示程序已退出
                        print("未检测到程序运行状态，准备启动程序")

                except KeyboardInterrupt as e:
                    print("检测到CTRL+C，准备退出程序!")
            startday = endday
            n_days = n_days + delta
            endday = n_days.strftime('%Y-%m-%d')

    def run(self, word):
        print('start OK!')
        self.p = subprocess.Popen("python {0} {1}".format(self.cmd, word))



app = Auto_Run(TIME, CMD)
