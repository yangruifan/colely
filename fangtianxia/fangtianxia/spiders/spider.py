# -*- coding: utf-8 -*-
import scrapy
import hashlib
from urllib import parse
from fangtianxia.items import FangtianxiaItem

class SpiderSpider(scrapy.Spider):
    name = 'spider'
    url = 'https://alaer.esf.fang.com/newsecond/esfcities.aspx'

    def get_md5(self, url):
        if isinstance(url, str):
            url = url.encode("utf-8")
        m = hashlib.md5()
        m.update(url)
        return m.hexdigest()

    def start_requests(self):
        yield scrapy.Request(url=self.url,
                             dont_filter=True,
                             )

    def parse(self, response):
        citylist = response.css("div.onCont ul li a::attr(href)").extract()
        citylist = set(citylist)
        for url in citylist:
            url = parse.urljoin(response.url, url)
            url = parse.urljoin(url, '/housing/')
            # url = "https://abazhou.esf.fang.com/housing/"
            yield scrapy.Request(url=url,
                                 dont_filter=True,
                                 callback=self.analysis_page)

    def analysis_page(self, response):
        houselist = response.css("div.houseList div.list.rel.mousediv dd p a.plotTit::attr(href)").extract()
        for houseurl in houselist:
            if 'com' in houseurl:
                yield scrapy.Request(url='http:'+ houseurl,
                                     dont_filter=True,
                                     callback=self.get_price,
                                     )
        next_url = response.css("#PageControl1_hlk_next::attr(href)").extract_first()
        if next_url == None:
            pass
        else:
            next_url = parse.urljoin(response.url, next_url)
            yield scrapy.Request(url=next_url,
                                 dont_filter=True,
                                 callback=self.analysis_page)

    def get_price(self, response):
        price = response.css('span.prib::text').extract_first()
        url = parse.urljoin(response.url, '/xiangqing/')
        yield scrapy.Request(url=url,
                             dont_filter=True,
                             meta={
                               'price': price,
                             },
                             callback=self.get_information)

    def get_information(self, response):
        item = FangtianxiaItem()
        url = response.url
        url_hash = self.get_md5(url=url)
        oldprice = ''
        nowprice = ''
        oldprice = response.meta['price']
        nowprice = response.css("span.red::text").extract_first()
        information = response.xpath("//div[@class='con_left']/div[2]/div[2]/dl/dd")
        xiaoqudizhi = ''
        lvhualv = ''
        wuyegongsi = ''
        jianzhujiegou = ''
        rongjilv = ''
        youbian = ''
        loudong = ''
        wuyefei = ''
        jianzhuniandai = ''
        kaifashang = ''
        jianzhumianji = ''
        fangwuzongshu = ''
        wuyeleibie = ''
        fujiaxinxi = ''
        zhandimianji = ''
        jianzhuleixing = ''
        chanquanmiansu = ''
        suoshuquyu = ''
        for infor in information:
            name = infor.css("dd strong::text").extract_first()
            text = infor.css("dd::text").extract_first()
            if text == None:
                text = infor.css("dd span::text").extract_first()
            if '小区地址' in name:
                xiaoqudizhi = text
            elif '绿' in name:
                lvhualv = text
            elif '物业公司' in name:
                wuyegongsi = text
            elif '结构' in name:
                jianzhujiegou = text
            elif '容' in name:
                rongjilv = text
            elif '邮' in name:
                youbian = text
            elif '楼栋总数' in name:
                loudong = text
            elif '物 业 费' in name:
                wuyefei = text
            elif '建筑年代' in name:
                jianzhuniandai = text
            elif '发' in name:
                kaifashang = text
            elif '建筑面积' in name:
                jianzhumianji = text
            elif '房屋总数' in name:
                fangwuzongshu = text
            elif '物业类别' in name:
                wuyeleibie = text
            elif '附加信息' in name:
                fujiaxinxi = text
            elif '占地面积' in name:
                zhandimianji = text
            elif '建筑类型' in name:
                jianzhuleixing = text
            elif '产权描述' in name:
                chanquanmiansu = text
            elif '所属区域' in name:
                suoshuquyu = text
            else:
                print(name)
        item['url'] = url
        item['url_hash'] = url_hash
        item['oldprice'] = oldprice
        item['nowprice'] = nowprice
        item['xiaoqudizhi'] = xiaoqudizhi
        item['lvhualv'] = lvhualv
        item['wuyegongsi'] = wuyegongsi
        item['jianzhujiegou'] = jianzhujiegou
        item['rongjilv'] = rongjilv
        item['youbian'] = youbian
        item['loudong'] = loudong
        item['wuyefei'] = wuyefei
        item['jianzhuniandai'] = jianzhuniandai
        item['kaifashang'] = kaifashang
        item['jianzhumianji'] = jianzhumianji
        item['fangwuzongshu'] = fangwuzongshu
        item['wuyeleibie'] = wuyeleibie
        item['fujiaxinxi'] = fujiaxinxi
        item['zhandimianji'] = zhandimianji
        item['jianzhuleixing'] = jianzhuleixing
        item['chanquanmiansu'] = chanquanmiansu
        item['suoshuquyu'] = suoshuquyu
        yield item

