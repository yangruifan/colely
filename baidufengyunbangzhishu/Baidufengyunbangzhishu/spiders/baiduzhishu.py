# -*- coding: utf-8 -*-
import scrapy
import time
from untils.commons import get_md5
from scrapy.http import Request
try:
    import  urlparse as parse
except:
    from urllib import parse
from items import YellowurlItem

class BaiduzhishuSpider(scrapy.Spider):
    name = 'baiduzhishu'
    allowed_domains = ['www']
    start_urls = ['http://top.baidu.com/boards?fr=topcategory_c1']
    # , 'http://top.sogou.com/movie/all_1.html'

    #将一个分类的小块html进行提取，提取出分类名称以及在这个分类下的url
    @staticmethod
    def baidipage_one_class(small_page):
        class_type = small_page.css("div h3 a::text").extract()
        movie_list = small_page.xpath("div/div[@class='links']/a/text()|div/div[@class='links']/a/@href").extract()
        movie_lists = []
        movie_lists.append(class_type[1])
        movie_lists.append(movie_list)
        return movie_lists   #以列表的形式返回 例[类别，[url，电影类别，url，电影类别，。。。。。。]]

    def parse(self, response):
        for i in range(1,len(response.css("#main div.all-list"))+1):
            one_class = response.css("#main div.all-list:nth-child({0})".format(i))
            url_list = self.baidipage_one_class(one_class)
            for i in range(0,len(url_list[1]),2):
                yield Request(url= parse.urljoin(response.url,url_list[1][i]),meta={"class_type_top1":url_list[0],"class_type_top2":url_list[1][i+1]},callback=self.baidupage,dont_filter=True)



    @staticmethod
    def baidipage_one_movie(small_page):
        movie_list = small_page.xpath("td[@class='keyword']/a[1]/text()|td[@class='last']/span/text()").extract()
        return movie_list



    def baidupage(self,response):
        movieitem = YellowurlItem()
        movie=[]
        list = response.css("table.list-table")
        small_page = list.xpath("//table/tr[2]")
        movie.append(self.baidipage_one_movie(small_page))
        small_page = list.xpath("//table/tr[4]")
        movie.append(self.baidipage_one_movie(small_page))
        small_page = list.xpath("//table/tr[6]")
        movie.append(self.baidipage_one_movie(small_page))
        long = len(list.css("table tr"))
        for i in range(8,long+1):
            small_page = list.css("tr:nth-child({0})".format(i))
            movie.append(self.baidipage_one_movie(small_page))
        for one_movie in movie:
            movieitem["class_type_top1"] = response.meta['class_type_top1']
            movieitem["class_type_top2"] = response.meta['class_type_top2']
            movieitem["name"] = one_movie[0]
            movieitem["name_hash"] = get_md5(one_movie[0])
            movieitem["baidu_number"] = one_movie[1]
            movieitem["create_time"] = time.strftime("%Y-%m-%d", time.localtime())
            movieitem["type"] = "百度风云榜"
            yield movieitem

