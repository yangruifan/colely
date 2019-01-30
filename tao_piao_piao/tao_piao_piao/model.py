"""
评论插入数据库
"""
from datetime import datetime
import logging

from hashlib import md5

import pymysql


def insert_comment(content: object, movie_url: object, comment_url: object, create_time: object, author: object,
                   movie_name: object, show_star: object, favor: object, sqlconfig: object) -> object:
    """
    将评论插进数据库
    :param content: 评论内容
    :param movie_url: 电影首页地址
    :param comment_url: 评论页地址
    :param create_time: 创建时间 形如2018-12-01
    :param fetch_time: 爬取时间 形如20181201
    :param author: 评论作者
    :return:
    """
    movie_hash, comment_hash, content_hash = (md5(i.encode(encoding='utf-8')).hexdigest() for i in
                                              (movie_url, comment_url, content))
    now = datetime.now()
    now_text = f'{now.year:0>4d}{now.month:0>2d}{now.day:0>2d}'
    conn = pymysql.connect(**sqlconfig, charset='utf8', use_unicode=True)
    try:
        conn.ping(reconnect=True)
    except pymysql.err.OperationalError:
        conn = pymysql.connect(**sqlconfig, charset='utf8', use_unicode=True)
    cursor = conn.cursor()
    logging.info(f'insert {content}, {movie_name}, {show_star}, {favor}, {create_time}, {author}, {sqlconfig}, {now_text}')
    try:
        cursor.execute('''
        INSERT INTO  spider_comment(page_url, page_url_hash, comment_url, comment_url_hash, content_hash, title, author,
            create_time, content, fetch_time, source, content_type, author_given_score, thumbs_up)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (movie_url, movie_hash, comment_url, comment_hash, content_hash, movie_name, author, create_time, content, now_text, '淘票票', 'short_comment', show_star, favor))
    except pymysql.err.IntegrityError:
        logging.error('检查到重复评论')
    except pymysql.err.InternalError:
        logging.error('文本编码导致内部错误')
    except pymysql.err.DatabaseError:
        logging.error('url太长，插不下')
    conn.commit()
    conn.close()
