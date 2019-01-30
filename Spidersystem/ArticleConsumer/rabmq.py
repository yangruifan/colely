#!/usr/bin/env python
# encoding:utf-8
# @Time   : 2018/12/8
# @Author : 茶葫芦
# @Site   : 
# @File   : rabmq.py
import pika
from config import *

class rbmq_production(object):

    def push_mq(self, content, exchange=""):
        credentials = pika.PlainCredentials('market', 'maizuo1221')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=rbmq_host,credentials=credentials
        ))
        self.channel = self.connection.channel()
        self.channel.basic_publish(exchange=exchange,
                                   routing_key=exchange + "key",  # 指定队列的关键字为，这里是队列的名字
                                   body=content,
                                   properties=pika.BasicProperties(delivery_mode=2, )
                                   )  # 往队列里发的消息内容
        self.connection.close()

        print("push message '%s' into rabbitmq exchange '%s'" % (content, exchange))
# if __name__ == '__main__':
#     p=rbmq_production()
#     p.push_mq(json.dumps({'extract_rule':'//article/a/@href','url':'http://www.shift.jp.org/cn/blog/page/2/'}),exchange=list_exchange_name)
#     # p.push_mq("hello2", exchange=list_exchange_name)

class rbmq_consumer(object):
    def __init__(self):
        credentials = pika.PlainCredentials('market', 'maizuo1221')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=rbmq_host, credentials=credentials
        ))
        self.channel = self.connection.channel()

    def pull_mq(self, callbackfun, queue, exchange):
        self.channel.exchange_declare(exchange=exchange,
                                      exchange_type='fanout')
        self.channel.queue_declare(queue=queue, durable=True)
        self.channel.queue_bind(exchange=exchange,
                                queue=queue)
        print(' [*] Waiting for logs. To exit press CTRL+C')

        self.channel.basic_consume(callbackfun,
                                   queue=queue,
                                   no_ack=True)

        self.channel.start_consuming()


def callbackfun(ch, method, properties, body):
    print("get message from rabbitmq exchange [%s] method is [%s],properties is [%s],body is [%s]" % (
    ch, method, properties, body.decode()))


if __name__ == '__main__':
    c = rbmq_consumer()
    c.pull_mq(callbackfun, list_queue_name, list_exchange_name)
