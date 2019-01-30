#!/usr/bin/env python
# encoding:utf-8
# @Time   : 2019/1/16
# @Author : 茶葫芦
# @Site   : 
# @File   : listProduction.py

from listProduction.rabmq import rbmq_production
import json
from config import *
import pymysql
from listProduction.SpiderTools import spiderTools
from listProduction.HiTime import HiTime


def gen_list(source_id):
    """
    用户输入信息后，将用户输入的信息转化成启动的初始信息。
    :return: 
    """
    p = rbmq_production()
    conn = pymysql.connect(**mysqlconf)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 以字典形式返回
    spt = spiderTools()
    try:
        cursor.execute("select * from adv_spider_source where id={0}".format(source_id))
    except Exception as e:
        print("根据sourceid查询source信息失败" + str(e))
    source = cursor.fetchone()
    last_index = source.get('last_index') if source.get('first_finished')==0 else source.get('index_to_monitor')
    # 得到将要爬取的链接，list中没有的插入（第一次），有的就标记为未爬取重爬。
    urls_gen = set([source.get('url_template').format(i) for i in range(2, last_index +1,source.get('page_index_step'))])
    try:
        cursor.execute("select url from adv_spider_list_link where url in {0}".format(tuple(urls_gen)))
    except Exception as e:
        print("根据sourceid查询list信息失败")
    stored = cursor.fetchall()
    if stored:
        not_stored = urls_gen - set([i.get('url') for i in stored])
    else:
        not_stored = urls_gen
    try:
        for i in not_stored:
            cursor.execute("insert into adv_spider_list_link(source_id,url,fetched,hashurl,create_time) values('{0}','{1}','{2}','{3}','{4}')".format(source_id, i,0,spt.md5(i),HiTime.Now()))
        cursor.execute("update adv_spider_list_link set fetched=0 where url in {0}".format(tuple(urls_gen)))
        conn.commit()
        print('数据插入成功')
    except Exception as e:
        conn.rollback()
        print('数据插入失败：' + str(source_id) + str(i))
        print('失败原因：' + str(e))
    for i in urls_gen:
        p.push_mq(json.dumps({'extract_list_rule': source.get('extract_list_rule'), 'url': i, 'source_id': source_id}),
                  exchange=list_exchange_name)
    return False


if __name__ == '__main__':
    gen_list(1)
