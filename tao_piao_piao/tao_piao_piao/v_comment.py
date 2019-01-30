"""
获得淘票票的大V评论
"""
import time

from selenium import webdriver
from selenium.webdriver import TouchActions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

import config as global_config


def get_in_v_comment(driver: webdriver.Chrome):
    """
    假设处于电影详情页面,
    得到大V评论
    """

    def get_comment_num(driver: webdriver.Chrome):
        return len(BeautifulSoup(driver.page_source, 'lxml').find_all('div', class_='list-item'))

    def scroll_down(driver: webdriver.Chrome):
        """
        向下滑动大V影评，知道不能滑动为止
        """
        comment_num = get_comment_num(driver)
        while True:
            driver.execute_script('''window.scrollTo(0, document.body.scrollHeight)''')
            time.sleep(2)
            new_num = get_comment_num(driver)
            if new_num == comment_num:
                print(new_num)
                break
            else:
                comment_num = new_num

    v_comment = driver.find_element_by_id('J_list')
    y_scale = v_comment.location['y']
    driver.execute_script(f'''window.scrollTo(0, {y_scale - 300})''')
    touch_action = TouchActions(driver)
    touch_action.tap(v_comment).perform()
    WebDriverWait(driver, global_config.time_out).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'grade'))
    )
    scroll_down(driver)
    comments = [{'comment': i.find('pre', class_='item-body').get_text(),
                 'grade': i.find('div', class_='grade').get_text()} for i in
                BeautifulSoup(driver.page_source, 'lxml').find_all('div', class_='list-item')]
    print(comments)
