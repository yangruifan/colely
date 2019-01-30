#!/usr/bin/env python
# encoding:utf-8
# @Time   : 2018/10/06
# @File   : config.py

import os

# IP白名单
whiteIPS = ['10.125.0.19', '127.0.0.1']

# 服务运行端口
Port = 12310

# application配置参数
settings = dict(
    static_path=os.path.join(os.path.dirname('__file__'), 'static'),
    template_path=os.path.join(os.path.dirname('__file__'), 'static'),
    debug=False,
    cookie_secret="2hcicVu+TqShDpfsjMWQLZ0Mkq5NPEW6Sk9fi0zsSt3A=",
)

# 队列信息
rbmq_host = '10.125.0.29'
list_queue_name = 'lists'
list_exchange_name = "listchange"

article_queue_name = 'articles'
article_exchange_name = "articlechange"

ipRedisConf = dict(
    host='10.125.0.7',
    port=6379,
    db=0,
    password='crs-hbnwcb9i:r@16samVW!jh',
    socket_connect_timeout=5
)

# 生产数据库
mysqlconf = dict(
    host='gz-cdb-l4r5h3m3.sql.tencentcdb.com',
    port=61928,
    db='market_spider',
    user='root',
    passwd='samVW!$#jh',
    charset='utf8',
    use_unicode=True
)

imgRedisConf = dict(
    host='10.125.0.7',
    port=6379,
    db=0,
    password='crs-hbnwcb9i:r@16samVW!jh',
    socket_connect_timeout=5
)


# 测试数据库信息
# imgRedisConf = dict(
#     host='47.106.148.36',
#     port=6379,
#     db=0,
#     password='1Q2W3E',
#     socket_connect_timeout=5
# )
# mysqlconf = dict(
#     host='47.106.148.36',
#     port=3306,
#     db='wx',
#     user='root',
#     passwd='1Q2W3E',
#     charset='utf8',
#     use_unicode=True
# )
