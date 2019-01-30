#!/usr/bin/env python
# encoding:utf-8
# @Time   : 2018/10/06
# @File   : FrameServer.py

import tornado.web, tornado.options, tornado.log
import tornado.ioloop
import urls, config
import logging

logger = logging.getLogger()
fm = tornado.log.LogFormatter(
    fmt='[%(asctime)s]%(color)s[%(levelname)s]%(end_color)s[%(module)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
tornado.log.enable_pretty_logging(logger=logger)  # 自己添加logger不用tornado自动生成的
logger.handlers[0].setFormatter(fm)


class Application(tornado.web.Application):
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
        self.logger = logger
        # self.redis= redis.StrictRedis(**config.redisconf)


def main():
    tornado.options.parse_command_line()
    app = Application(urls.rute_urls,
                      **config.settings
                      )
    app.listen(config.Port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    logging.info("web server start running...")
    main()
