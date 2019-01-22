from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pymysql
import datetime
import hashlib
import logging
first_url = 'https://dianying.taobao.com/showList.htm?&n_s=new'
url = 'https://h5.m.taopiaopiao.com/app/moviemain/pages/show-detail/index.html?showid={index}'
movieid = []
ua = UserAgent(verify_ssl=False)
HEADERS = {

}
my_sql = {
    'db': 'market_spider',
    'user': 'root',
    'password': 'samVW!$#jh',
    'host': 'gz-cdb-l4r5h3m3.sql.tencentcdb.com',
    'port': 61928
}

class TAOPIAOPIAO():
    def __init__(self):
        self.conn = pymysql.connect(**my_sql, charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def get_driver(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('mobileEmulation', {'deviceName': 'iPhone 8'})
        options.add_argument("--headless")  # 使用headless 无界面形态
        options.add_argument('--disable-gpu')  # 禁用gpu
        options.add_argument('-no-sandbox')  # 禁用沙箱
        chrome = webdriver.Chrome(chrome_options=options)
        chrome.implicitly_wait(10)
        return chrome

    def get_md5(self, data):
        if isinstance(data, str):
            data = data.encode("utf-8")
        m = hashlib.md5()
        m.update(data)
        return m.hexdigest()

    def get_movieid(self, linkdata):
        reg = r'showId=(\d{1,8})&'
        idnum = re.search(reg, linkdata)
        return idnum.group(1)

    def get_movie_list(self):
        HEADERS['UserAgent'] = ua.random
        response = requests.get(url=first_url, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'lxml')
        datas = soup.find_all('div', class_='tab-movie-list')[1]
        datas = datas.find_all('div', class_='movie-card-wrap')
        for data in datas:
            link = data.find('a', class_='movie-card-soon')['href']
            movie_id = self.get_movieid(link)
            movieid.append(movie_id)

    def get_time(self, data):
        reg = r'(\d{4}-?\d{0,2}-?\d{0,2})'
        movietime = re.search(reg, data)
        try:
            return movietime.group(1)
        except:
            return '0000-00-00'

    def get_type(self, data):
        lists = re.split('/', data)
        # print(lists)
        if "分钟" in lists[-1]:
            movietime = lists[-1].replace('分钟', '').strip()
            whereshow = lists[-2].strip()
            movietype = ','.join(lists[0: -2])
        else:
            movietime = 0
            whereshow = lists[-1].strip()
            movietype = ','.join(lists[0: -1])
        return movietime, whereshow, movietype

    def get_num(self, data):
        reg = '([0-9.万]{0,10})'
        num = re.search(reg, data)
        try:
            return num.group(1)
        except:
            return '暂无'

    def input_MYSQL(self, moviename, movieName, movie_hash, movietime, whereshow, movietype, showtime, wantsee, content, autor, fetch_time):
        try:
            self.conn.ping(reconnect=True)
        except:
            self.conn = pymysql.connect(**my_sql, charset='utf8', use_unicode=True)
            self.cursor = self.conn.cursor()
        sql = "select * from movie_want where movie_hash='{}'".format(movie_hash)
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        if results == ():
            sql = """INSERT INTO movie_want(movie_chinese,movie_english,movie_hash,movie_long,movie_type,where_show,show_time,how_many,
            content,autor,fetch_time,source)
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            self.cursor.execute(sql, (moviename, movieName, movie_hash, movietime, movietype, whereshow, showtime, wantsee, content,
                                      autor, fetch_time, "淘票票"))

            self.conn.commit()
            print('{}插入成功。'.format(moviename))
        else:
            print('{}数据已存在。'.format(moviename))

    def close_sql(self):
        self.conn.close()

    # 动作 / 冒险 / 喜剧 / 科幻 / 美国 / 119分钟
    def analysis(self, html):
        soup = BeautifulSoup(html, 'lxml')
        moviename = soup.find('p', class_='chinese').get_text()
        movieName = soup.find('p', class_='source').get_text()
        try:
            movie_hash = self.get_md5(moviename)
        except:
            movie_hash = self.get_md5(movieName)
        moviedata = soup.find_all('p', class_='show-intro')
        dataone = moviedata[0].get_text()
        movietime, whereshow, movietype = self.get_type(dataone)
        datatwo = moviedata[1].get_text()
        showtime = self.get_time(datatwo)
        wantsee = self.get_num(moviedata[2].get_text())
        try:
            content = soup.find('section', class_='show-desc').find('p')['data-content']
        except AttributeError:
            content = ''
        try:
            artistlist = soup.find('div', class_='show-artist-list').find_all('a')
            autor = ''
            for artist in artistlist:
                name = artist.find('dl').text
                autor = autor + name + ','
        except AttributeError:
            autor = ''
        fetch_time = datetime.datetime.now().strftime('%Y-%m-%d')
        self.input_MYSQL(moviename, movieName, movie_hash, movietime, whereshow, movietype, showtime, wantsee, content, autor, fetch_time)

    def get_moviepage(self, driver):
        for movie in movieid:
            movieurl = url.format(index=movie)
            driver.get(movieurl)
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.chinese')))
            self.analysis(driver.page_source)

    def driver_close(self, driver):
        driver.close()


def main():
    pro = TAOPIAOPIAO()
    pro.get_movie_list()
    driver = pro.get_driver()
    pro.get_moviepage(driver)
    pro.close_sql()
    pro.driver_close(driver)


if __name__ == '__main__':
    main()
