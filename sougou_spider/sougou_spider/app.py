from scrapy import cmdline
import sys


class runs():
    def __init__(self, name):
        cmdline.execute('scrapy crawl spider -a word={}'.format(name).split())


runs(name=str(sys.argv[1]))

