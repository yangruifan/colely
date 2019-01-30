import time
import random
import re
import logging
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import TouchActions
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

from common import get_driver
from . import config, v_comment
import config as global_config
from .model import insert_comment
from selenium.common.exceptions import NoSuchElementException


def get_in_mv_list(driver: webdriver.Chrome, num: str):
    """假设driver已经设置好，进入电影列表(当前城市: 北京)"""
    logging.info('点击城市进入电影列表')
    driver.get(config.portal_url)

    try:
        WebDriverWait(driver, global_config.time_out).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.hot')))
    except:
        WebDriverWait(driver, global_config.time_out).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '#J_City')))
        driver.find_element_by_id('J_City').click()
    # city_element = driver.find_element_by_css_selector('.hot .city-item')
    city_element = driver.find_element_by_xpath('//*[@id="热门"]/ul/li[{}]'.format(num))
    # print(city_element)
    city_element.click()
    while True:
        movie_items = driver.find_elements_by_class_name(config.movie_item_class)
        driver.execute_script(f'''window.scrollTo(0, document.body.scrollHeight)''')
        time.sleep(config.ajax_wait)
        new_items = driver.find_elements_by_class_name(config.movie_item_class)
        if len(new_items) == len(movie_items):
            break


def get_in_comment(driver: webdriver.Chrome):
    """
    假设已经进入电影详情
    进入电影评论页
    """
    logging.info('进入评论页')
    view_all_css = '.show-comments .view-all'  # '.show-desc-expand-btn'
    WebDriverWait(driver, global_config.time_out).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, view_all_css)))
    view_all = driver.find_element_by_css_selector(view_all_css)
    y_scale = view_all.location['y']
    driver.execute_script(f'''window.scrollTo(0, {y_scale - random.uniform(*config.random_length)})''')
    touch_action = TouchActions(driver)
    touch_action.tap(view_all).perform()


def load_comment(driver: webdriver.Chrome):
    """
    使得页面加载评论
    """
    logging.info('加载评论')

    def get_comment_num(driver: webdriver.Chrome) -> int:
        return len(BeautifulSoup(driver.page_source, 'lxml').find_all('div', class_=config.comment_class))

    def sniff_load(driver: webdriver.Chrome):
        comment_num = get_comment_num(driver)
        driver.execute_script('''window.scrollTo(0, document.body.scrollHeight - 300)''')
        time.sleep(1)
        driver.execute_script('''window.scrollTo(0, document.body.scrollHeight)''')
        time.sleep(1)
        for i in range(20):
            time.sleep(1)
            new_num = get_comment_num(driver)
            if new_num > comment_num:
                break

    driver.execute_script('''window.scrollTo(0, document.body.scrollHeight)''')
    sniff_load(driver)


def load_all_comment(driver: webdriver.Chrome):
    """
    假设一斤处于评论页面初始状态
    加载大量评论，直到一半的评论内容都是重复的为止
    """
    logging.info('等待加载所有评论')
    start_time = time.time()
    def should_end(driver: webdriver.Chrome):
        soup = BeautifulSoup(driver.page_source, 'lxml')
        comments = [i.find('div', class_=config.comment_content_class).get_text()
                    for i in soup.find_all('div', class_=config.comment_class)]
        logging.info(f'加载评论...重复率{len(comments) / len(set(comments))}, 总数量{len(comments)}')
        end_text = '底线' in soup.find('div', class_='load-more').get_text()
        return (len(comments) / len(set(comments)) > 2) or (len(comments) >= 490) or end_text

    while not should_end(driver):
        logging.info('load comment...')
        load_comment(driver)
        end_time = time.time()
        if int(end_time - start_time) > 150:
            break


def get_movie_tag(driver: webdriver.Chrome):
    """
    获得观众影评标签
    """
    soup = BeautifulSoup(driver.page_source, 'lxml')
    return [i.get_text() for i in soup.find('ul', id='tabUl').find_all('li') if re.match(r'^\d+$', i['data-code'])]


def get_comments_info(driver: webdriver.Chrome):
    """
    假设评论已经加载完毕，获得页面上所有的评论信息
    """

    def get_time(cm_node):
        try:
            time_text = cm_node.find('div', class_='comment-publish-time').get_text()
            search = re.search(r'(\d{2})-(\d{2})', time_text)
            date, month = (search.group(i) for i in range(1, 3))
            return f'2018-{month}-{date}'
        except AttributeError:
            now = datetime.now()
            return f'{now.year}-{now.month:0>2d}-{now.day:0>2d}'

    def get_comment(cm_node):
        return cm_node.find('div', class_='content').get_text()

    def get_star(cm_node):
        try:
            return cm_node.find('div', class_='remark-num').get_text()
        except AttributeError:
            return 0

    def get_favor(cm_node):
        try:
            num = cm_node.find('span', class_='fn-num').get_text()
            if '赞' in num:
                num = 0
            return num
        except:
            return 0
    soup = BeautifulSoup(driver.page_source, 'lxml')
    return [{'name': i.find('div', class_='comment-user-nickname').get_text(),
             'content': get_comment(i),
             'time': get_time(i),
             'show_star': get_star(i),
             'favor': get_favor(i),
             }
            for i in soup.find_all('div', class_='single-comment')]


def run_tpp_spider():
    driver = get_driver()
    ii = 0
    while True:
        ii += 1
        try:
            while True:
                get_in_mv_list(driver, ii)
                mv_list_soup = BeautifulSoup(driver.page_source, 'lxml')
                movie_links = [{'link': i['href'], 'name': i.find('div').get_text()}
                               for i in mv_list_soup.find_all('a', class_=config.movie_item_class)]
                if movie_links:
                    break

            for i in movie_links:
                driver.get(i['link'])
                movie_name = BeautifulSoup(driver.page_source, 'lxml').find('div', class_='movie-name').get_text()
                movie_page = driver.current_url
                try:
                    get_in_comment(driver)
                except TimeoutException:
                    logging.error('评论不足')
                    continue
                comment_url = driver.current_url
                # tags = get_movie_tag(driver)  # 标签，数据库无字段可存
                load_all_comment(driver)
                comment_info = get_comments_info(driver)
                for info in comment_info:
                    insert_comment(info['content'], movie_page, comment_url, info['time'], info['name'], movie_name, info['show_star'], info['favor'],
                                   global_config.my_sql)

        except NoSuchElementException:
            driver.close()