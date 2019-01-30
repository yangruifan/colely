#!/usr/bin/env python
# encoding:utf-8
# @Time   : 2018/10/06
# @File   : funcs.py

from baseHandler import BaseHandler
import json
import pymysql
import config
from listProduction import listProduction


class sourceSave(BaseHandler):
    """
    爬虫相关信息添加入库
    """
    def post(self, *args, **kwargs):
        jsDict = json.loads(self.request.body.decode())
        self.conn = pymysql.connect(**config.mysqlconf)
        self.cursor = self.conn.cursor()
        query_id = ""
        idstr = jsDict.get('id', '')
        name = jsDict.get('name', '')
        index_to_monitor = jsDict.get('index_to_monitor', '0')
        last_index = jsDict.get('last_index', '')
        first_finished = jsDict.get('first_finished', '')
        page_size = jsDict.get('page_size', '')
        page_index_step = jsDict.get('page_index_step', '')
        create_time = jsDict.get('create_time', '')
        extract_list_rule = jsDict.get('extract_list_rule', '')
        extract_title_rule = jsDict.get('extract_title_rule', '')
        extract_content_rule = jsDict.get('extract_content_rule', '')
        extract_author_rule = jsDict.get('extract_author_rule', '')
        extract_crtime_rule = jsDict.get('extract_crtime_rule', '')
        ad_rule = jsDict.get('ad_rule', '')
        root_url = jsDict.get('root_url', '')
        is_active = jsDict.get('is_active', '')
        url_template = jsDict.get('url_template', '')
        exists_list = jsDict.get('exists_list', '')
        if idstr:
            self.log.info(f"开始更新id:{idstr} name:{name}")
            try:
                update_sql = f'update adv_spider_source set name = "{name}",index_to_monitor = "{index_to_monitor}",last_index = "{last_index}",first_finished = {first_finished},page_size = "{page_size}",page_index_step = "{page_index_step}",create_time = "{create_time}",extract_list_rule = "{extract_list_rule}",extract_title_rule = "{extract_title_rule}",extract_content_rule = "{extract_content_rule}",extract_author_rule = "{extract_author_rule}",extract_crtime_rule = "{extract_crtime_rule}",ad_rule = "{ad_rule}",root_url = "{root_url}",is_active = {is_active},url_template = "{url_template}",exists_list = {exists_list} where id = {idstr}'
                print(update_sql)
                rows = self.cursor.execute(update_sql)
                query_id = idstr
                print(rows)
                self.conn.commit()
                self.log.info(f"更新id:{idstr} name:{name}成功")
            except Exception as e:
                self.conn.rollback()
                self.log.info(f"更新id:{idstr} name:{name}失败，更新参数：")
                self.log.info(f"{str(e)}--{jsDict}")
        else:
            self.log.info(f"开始插入id:{idstr} name:{name}")
            try:
                insert_sql = f'insert into adv_spider_source(name,index_to_monitor,last_index,first_finished,page_size,page_index_step,create_time,extract_list_rule,extract_title_rule,extract_content_rule,extract_author_rule,extract_crtime_rule,ad_rule,root_url,is_active,url_template,exists_list) values ("{name}",{index_to_monitor},"{last_index}",{first_finished},"{page_size}","{page_index_step}","{create_time}","{extract_list_rule}","{extract_title_rule}","{extract_content_rule}","{extract_author_rule}","{extract_crtime_rule}","{ad_rule}","{root_url}",{is_active},"{url_template}",{exists_list})'
                print(insert_sql)
                rows = self.cursor.execute(insert_sql)
                query_id = self.cursor.lastrowid
                self.conn.commit()
                self.log.info(f"插入id:{idstr} name:{name} 成功")
            except Exception as e:
                self.conn.rollback()
                self.log.info(f"插入id:{idstr} name:{name}失败，更新参数：")
                self.log.info(f"错误原因：{str(e)}")
                self.write(json.dumps({'errcode': -1, 'msg': str(e)}))
        if query_id:
            self.write(json.dumps({'errcode': 0, 'msg': query_id}))
        else:
            self.write(json.dumps({'errcode': -1, 'msg': "数据操作出错"}))


class query_by_id(BaseHandler):
    """
    根据id进行爬虫查询
    """
    def get(self):
        jsDict = json.loads(self.request.body.decode())
        sourceid = jsDict.get('source_id')
        self.conn = pymysql.connect(**config.mysqlconf)
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

        try:
            query_str = f'select * from adv_spider_source where id={sourceid}'
            rows = self.cursor.execute(query_str)
            ret=self.cursor.fetchall()
            self.write(json.dumps({'errcode': 0, 'msg': ret}))
        except Exception as e:
            self.log.info(f"查询错误原因：{str(e)}")
            self.write(json.dumps({'errcode': -1, 'msg': str(e)}))



class genList(BaseHandler):
    """
    爬虫规则制定好后调用此方法进行生成链接开始爬取，每日定时任务也由此发起
    """
    def post(self, *args, **kwargs):
        jsDict = json.loads(self.request.body.decode())
        sourceid = jsDict.get('source_id')
        listProduction.gen_list(sourceid)
        self.write(json.dumps({'errcode': 0, 'msg': sourceid}))


class status_error_source(BaseHandler):
    """
    获取状态异常爬虫供前端展示
    """
    def get(self):
        self.conn = pymysql.connect(**config.mysqlconf)
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            select_sql = f'select status,status_should_be,source_name from spider_source_type where status > status_should_be'
            rows = self.cursor.execute(select_sql)
            ret=self.cursor.fetchall()
            self.write(json.dumps({'errcode': 0, 'msg': ret}))
        except Exception as e:
            self.log.info(f"查询错误原因：{str(e)}")
            self.write(json.dumps({'errcode': -1, 'msg': str(e)}))



if __name__ == '__main__':
    pass
