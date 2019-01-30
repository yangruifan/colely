#!/usr/bin/env python
# encoding:utf-8
# @Time   : 2018/10/06
# @File   : urls.py

import funcs
'''
路由列表
'''

rute_urls = [
    (r'/api/v1/sourceSave', funcs.sourceSave),
    (r'/api/v1/genlist', funcs.genList),
    (r'/api/v1/status_error_source', funcs.status_error_source),

]
