# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from spider_list.Operate_datebase_table import Operate_datebase_table
try:
    import urlparse as parse
except:
    from urllib import parse
from spider_list.items import SpiderListItem

class SpiderSpider(scrapy.Spider):
    name = 'spider'

    def start_requests(self):
        url = "https://www.qidian.com/"
        yield Request(url=url,
                      dont_filter=True,
                      priority=1)

    def parse(self, response):
        spideritem = SpiderListItem()
        connect = Operate_datebase_table("adv_spider_source")  # 链接文章列表
        try:
            # (('你好，之华',), ('触不可及',), ('李茶的姑妈',))
            datas = connect.selectTable(
                "(id,page_index_step,last_index,index_to_monitor,url_template,root_url,first_fininshed)")  # 查找列表url是否有待爬
        except:
            print("查询列表url错误！")

        # updata_connect.updateTale({'fetched': '1', }, 'url="{}"'.format(response.url))

        for datas_one in datas:
            connect.updateTale({'first_fininshed': '1', }, 'id={}'.format(datas_one[0]))
            id = datas_one[0]
            page_index_step = datas_one[1]
            last_index = datas_one[2]
            index_to_momitor = datas_one[3]
            url_template = datas_one[4]
            root_url = datas_one[5]
            first_finished = datas_one[6]
            if first_finished == 0:
                for i in range(1, (last_index // page_index_step) + 1):
                    if i != 1:
                        url = url_template.format(index=i * page_index_step)
                        url = parse.urljoin(root_url, url)
                    else:
                        url = root_url
                    spideritem["url"] = url
                    spideritem["flag"] = 0
                    spideritem["source_id"] = str(id)
                    yield spideritem
                    # yield self.make_requests_from_url(spideritem)

            else:
                for i in range(1, (index_to_momitor // page_index_step) + 1):
                    if i != 1:
                        url = url_template.format(index=i * page_index_step)
                        url = parse.urljoin(root_url, url)
                    else:
                        url = root_url
                    spideritem["url"] = url
                    spideritem["flag"] = 0
                    spideritem["source_id"] = str(id)
                    yield spideritem
                    # yield self.make_requests_from_url(spideritem)
