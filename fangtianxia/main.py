__author__ = 'colely'
from scrapy.cmdline import execute
import sys
import os

# print(sys.path.append(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(r'G:\python软件\暑假爬虫提升\scrapy\ArticleSpider\ArticleSpider')
execute(['scrapy', 'crawl', 'spider'])