# -*- coding: utf-8 -*-
import scrapy
try:
    import  urlparse as parse
except:
    from urllib import parse
from scrapy.http import Request
from sougoupaihangbang.items import SougoupaihangbangItem
from sougoupaihangbang.untils.commons import get_md5
import time
class SougouzhishuSpider(scrapy.Spider):
    name = 'sougouzhishu'
    allowed_domains = ['top.sogou.com']
    start_urls = ['http://top.sogou.com/home.html']

    def parse(self, response):
        class_list = response.xpath("//div[@class='menu']/a/text()|//div[@class='menu']/a/@href").extract()
        for i in range(2,len(class_list),2):
            url = parse.urljoin(response.url,class_list[i])
            # print(url)
            yield Request(url= url,meta={"topic_parent":class_list[i+1]},callback=self.one_class_page,dont_filter=True)


    def one_class_page(self,response):
        topic_page_lists = response.xpath("//div[@class='snb']/a/text()|//div[@class='snb']/a/@href").extract()
        for i in range(0,len(topic_page_lists),2):

            url = parse.urljoin(response.url,topic_page_lists[i])
            # print(url,topic_page_lists[i+1])
            yield Request(url= url,meta={"topic_parent":response.meta['topic_parent'],"topic":topic_page_lists[i+1]},callback= self.one_page_analysis,dont_filter=True)
            url = url[0:-6] + '2.html'
            yield Request(url= url,meta={"topic_parent":response.meta['topic_parent'],"topic":topic_page_lists[i+1]},callback= self.one_page_analysis,dont_filter=True)
            url = url[0:-6] + '3.html'
            yield Request(url= url,meta={"topic_parent":response.meta['topic_parent'],"topic":topic_page_lists[i+1]},callback= self.one_page_analysis,dont_filter=True)



    @staticmethod
    def analysis(data):
        list = []
        name = data.css("span.s2 p.p1 a::text").extract_first()
        sougou_number = data.css("span.s3::text").extract_first()
        list.append(name)
        list.append(sougou_number)
        return list

    def one_page_analysis(self,response):
        if response.status != 200:
            pass
        else:
            sougouzhishuitem = SougoupaihangbangItem()
            all_data = response.css("ul.pub-list li")
            for one_data in all_data:
                datas = self.analysis(one_data)
                sougouzhishuitem["name"] = datas[0]
                sougouzhishuitem["class_type_top1"] = response.meta['topic_parent']
                sougouzhishuitem["class_type_top2"] = response.meta['topic']
                sougouzhishuitem["sougou_number"] = datas[1]
                sougouzhishuitem["name_hash"] = get_md5(datas[0])
                sougouzhishuitem["type"] = "搜狗排行榜"
                sougouzhishuitem["create_time"] = time.strftime("%Y-%m-%d", time.localtime())
                yield sougouzhishuitem

