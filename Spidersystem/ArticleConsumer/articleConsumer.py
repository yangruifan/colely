#!/usr/bin/env python
# encoding:utf-8
# @Time   : 2019/1/16
# @Author : 茶葫芦
# @Site   : 
# @File   : listConsumerbak.py

import threading
from lxml import etree
from config import *
from rabmq import rbmq_consumer
import json
import pymysql
import html
import time
from SpiderTools import spiderTools
from HiTime import HiTime

globalvals = {'threadcounts': 0, 'maxthreadcounts': 20}  # 当前线程数：threadcounts  允许最大线程数：maxthreadcounts

def fetcharticle(listargs):
    """
    根据监听到的栏目列表抓取文章链接入库，入rabmq
    :param listargs:
    :return:
    """
    global globalvals
    conn = pymysql.connect(**mysqlconf)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 以字典形式返回
    article_urls = listargs.get('article_urls')
    source_id = listargs.get('source_id')
    spt=spiderTools()
    try:
        cursor.execute(
            "select name,extract_title_rule,extract_author_rule,extract_content_rule,extract_crtime_rule from adv_spider_source where id={0}".format(
                source_id))
    except Exception as e:
        print("根据sourceid查询标题，内容提取规则失败")
    source = cursor.fetchone()
    for url in article_urls:
        resp = spt.sendSpiderRequest(url)
        if resp == "":
            print("url爬虫重试多次无效，链接未处理" + url)
            return
        text=resp.text
        xml_tree = etree.HTML(text)
        try:
            title_match = xml_tree.xpath(source.get('extract_title_rule'))
            title = title_match[0] if isinstance(title_match, list) and len(title_match) else title_match
            author_match = xml_tree.xpath(source.get('extract_author_rule')) if source.get('extract_author_rule') else ""
            author = author_match[0] if isinstance(author_match, list) and len(author_match) else author_match
            crtime_match = xml_tree.xpath(source.get('extract_crtime_rule')) if source.get('extract_crtime_rule') else int(time.time())
            crtime = crtime_match[0] if isinstance(crtime_match, list) and len(crtime) else crtime_match
            content =html.unescape(etree.tostring(xml_tree.xpath(source.get('extract_content_rule'))[0], method='html', encoding='utf-8').decode())
        except Exception as e:
            print("解析页面出错")
            return
        spt.saveArticle(url=url,title=title,author=author,content=content,status=1,create_time=crtime,source=source.get('name'))
        try:
            # 将已爬取的listurl进行标记及记录爬取时间
            cursor.execute(
                "update adv_spider_article_link set fetched=1,fetch_time='{0}' where hashurl='{1}'".format(HiTime.Now(),spt.md5(url)))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print('文章爬取时间及标志更新失败：source_id：' + str(source_id) + ',url: '+url+str(e))
    globalvals['threadcounts'] = globalvals['threadcounts'] - 1


def rabcallback(ch, method, properties, body):
    """
    rbbitmq监听到文章信息后回调此函数（采用多线程提高处理速度）
    :param ch:
    :param method:
    :param properties:
    :param body:
    :return:
    """
    print("get message from rabbitmq exchange [%s] method is [%s],properties is [%s],body is [%s]" % (
        ch, method, properties, body.decode()))
    global globalvals
    while True:
        if globalvals['threadcounts'] < globalvals['maxthreadcounts']:
            break
    t = threading.Thread(target=fetcharticle, args=(json.loads(body.decode()),))
    t.setDaemon(True)
    globalvals['threadcounts'] = globalvals['threadcounts'] + 1
    t.start()


if __name__ == '__main__':
    rc = rbmq_consumer()
    rc.pull_mq(rabcallback, article_queue_name, article_exchange_name)
