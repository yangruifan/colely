#!/usr/bin/env python
# encoding:utf-8
# @Time   : 2018/10/06
# @File   : baseHandler.py

from tornado.web import RequestHandler
from config import whiteIPS


class BaseHandler(RequestHandler):
    """封装RequesetHandler基类,通用方法自动调用"""

    @property
    def db(self):
        """作为RequestHandler对象的db属性"""
        return self.application.db

    @property
    def log(self):
        """作为RequestHandler对象的logger属性"""
        return self.application.logger

    # @property
    # def cursor(self):
    #     return self.application.cursor
    #
    # @property
    # def conn(self):
    #     return self.application.conn
    # @property
    # def redis(self):
    #     return self.application.redis

    def prepare(self):
        if self.request.remote_ip not in whiteIPS:
            self.log.info("非白名单请求，已拒绝，请求ip："+self.request.remote_ip)
            self.write_error(404)
