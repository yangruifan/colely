_author = 'colely'

from selenium import webdriver as web
import json
import hashlib
import time
from zhishuinformation.settings import BAIDUUSER, BAIDUPASSWORD


def get_md5(data):
    if isinstance(data, str):
        data = data.encode("utf-8")
    m = hashlib.md5()
    m.update(data)
    return m.hexdigest()

class get_cookies():
    """
    #启动selenium实现登陆操作获取cookies的到访问权限
    :return:
    """
    def __init__(self):

        self.driver = web.Chrome()
        self.driver.get("http://index.baidu.com/#/")

        # self.flag = input("请输入 1 并回车。\n")
        # cookies = self.driver.get_cookies()

    def get_cookie(self):

        self.driver.find_element_by_xpath('//span[@class="username-text"]').click()
        time.sleep(2)
        self.driver.find_element_by_id('TANGRAM__PSP_4__userName').send_keys(BAIDUUSER)
        self.driver.find_element_by_id('TANGRAM__PSP_4__password').send_keys(BAIDUPASSWORD)
        time.sleep(20)
        # self.driver.find_element_by_id('TANGRAM__PSP_4__submit').click()
        time.sleep(5)
        cookies = self.driver.get_cookies()
        cookies = json.dumps(cookies)
        with open('cookies.txt', 'w') as f:
            f.write(cookies)

    def close_driver(self):
        self.driver.close()


if __name__ == '__main__':
    cookie = get_cookies()
    cookie.get_cookie()
    cookie.close_driver()