#!/usr/bin/env python
# encoding:utf-8
# @Time   : 2019/1/16
# @Author : 茶葫芦
# @Site   : 
# @File   : listConsumerbak.py

import threading
from lxml import etree
from config import *
from rabmq import rbmq_consumer, rbmq_production
import json
import pymysql
from HiTime import HiTime
from SpiderTools import spiderTools
from urllib import parse

globalvals = {'threadcounts': 0, 'maxthreadcounts': 20}  # 当前线程数：threadcounts  允许最大线程数：maxthreadcounts


def savearticleurls(source_id, article_urls, list_url):
    """
    提取到的文章链接入mysql库
    :param article_urls:
    :return:
    """
    conn = pymysql.connect(**mysqlconf)
    cursor = conn.cursor()
    spt = spiderTools()
    try:
        for url in article_urls:
            cursor.execute(
                '''INSERT INTO adv_spider_article_link(fetched,create_time,source_id,url,hashurl) VALUES (%s,%s,%s,%s,%s)''',
                (0, HiTime.Now(), source_id, url, spt.md5(url))
            )
        # 将已爬取的listurl进行标记及记录爬取时间
        cursor.execute(
            "update adv_spider_list_link set fetched=1,fetch_time='{0}' where hashurl='{1}'".format(HiTime.Now(),
                                                                                                    spt.md5(list_url)))
        conn.commit()
        print('数据插入成功：' + str(source_id) + str(article_urls))
        return True
    except Exception as e:
        conn.rollback()
        print('数据插入失败：' + str(source_id) + str(article_urls))
        print('失败原因：' + str(e))
        return False


def pusharticles(argsjson):
    """
    把提取到的文章链接入rabbitmq中
    :return:
    """
    rp = rbmq_production()
    rp.push_mq(argsjson, exchange=article_exchange_name)


def fetchlist(listargs):
    """
    根据监听到的栏目列表抓取文章链接入库，入rabmq
    :param listargs:
    :return:
    """
    global globalvals
    spt = spiderTools()
    list_url = listargs.get('url')
    extract_rule = listargs.get('extract_list_rule')
    source_id = listargs.get('source_id')
    resp = spt.sendSpiderRequest(url=list_url)
    if resp == "":
        print("url爬虫重试多次无效，链接未处理" + list_url)
        return
    article_urls = etree.HTML(resp.text).xpath(extract_rule)
    article_urls=[parse.urljoin(list_url,i) for i in article_urls]
    savearticleurls(source_id, article_urls, list_url)
    pusharticles(json.dumps({'source_id': source_id, 'article_urls': article_urls}))
    globalvals['threadcounts'] = globalvals['threadcounts'] - 1


def rabcallback(ch, method, properties, body):
    """
    rbbitmq监听到栏目信息后回调此函数（采用多线程提高处理速度）
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
    t = threading.Thread(target=fetchlist, args=(json.loads(body.decode()),))
    t.setDaemon(True)
    globalvals['threadcounts'] = globalvals['threadcounts'] + 1
    t.start()


if __name__ == '__main__':
    rc = rbmq_consumer()
    rc.pull_mq(rabcallback, list_queue_name, list_exchange_name)
