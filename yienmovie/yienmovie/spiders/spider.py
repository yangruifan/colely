# -*- coding: utf-8 -*-
import scrapy
import json
import datetime
from yienmovie.items import YienmovieItem, PeerItem
from yienmovie.settings import COMPANY_FROM


class SpiderSpider(scrapy.Spider):
    name = 'spider'

    def start_requests(self):
        self.starttime = datetime.date.today()
        starttime = datetime.date.today()
        endtime = starttime - datetime.timedelta(days=365)
        for i in range(12):
            url = 'http://ebotapp.entgroup.cn/API/DataBox/Company/CompanyBoxOfficeByDate'
            data = {
                'PageIndex': '1',
                'PageSize': '1000',
                'Order': '201',
                'OrderType': 'DESC',
                'Index': '101,102,201,203,604',
                'ServicePrice': '1',
                'sDate': str(starttime),
                'eDate': str(starttime),
                # 'sDate': '2004-01-01',
                # 'eDate': '2004-12-30',
            }
            starttime = endtime
            endtime = starttime - datetime.timedelta(days=365)
            yield scrapy.FormRequest(url=url, method='POST', formdata=data)


    def parse(self, response):
        response_page = json.loads(response.text)
        Companydatas = response_page['Data']['Table2']

        url = 'http://ebotapp.entgroup.cn/API/DataBox/Company/CompanyInvestCinema'
        starttime = datetime.date.today()
        endtime = starttime - datetime.timedelta(days=365)
        for i in range(50):
            for Company in Companydatas:
                Companyname = Company['CompanyName']
                CompanyID = Company['CompanyID']
                data = {
                    'Company': str(CompanyID),
                    'PageIndex': '1',
                    'PageSize': '100',
                    'DateSort': 'Self',
                    # 'Date': '2018-10-16,2019-01-16',
                    'sDate': str(endtime),
                    'eDate': str(starttime),
                }
                yield scrapy.FormRequest(url=url,
                                         method='POST',
                                         formdata=data,
                                         meta={'CompanyID': CompanyID,
                                               'Companyname': Companyname},
                                         callback=self.analysis_page)
                data1 = {
                    'OrgID': str(CompanyID),
                    'OrgType': '3',
                }
                url1 = 'http://ebotapp.entgroup.cn/API/BaseInfo/BaseInfo/GetOrgBaseInfoByID'
                yield scrapy.FormRequest(url=url1,
                                         method='POST',
                                         formdata=data1,
                                         meta={'CompanyID': CompanyID,
                                               'Companyname': Companyname},
                                         callback=self.analysis)
            starttime = endtime
            endtime = starttime - datetime.timedelta(days=365)

    def analysis(self, response):
        item = PeerItem()
        response_page = json.loads(response.text)
        ACompanyname = response.meta['Companyname']
        ACompanyID = response.meta['CompanyID']
        Companydatas = response_page['Data']['Table2']
        for Company in Companydatas:
            CompanyId = Company['CompanyId']
            CompanyName = Company['CompanyName']
            Num = Company['Num']
            CompanyType = Company['CompanyType']

            item['Companyname'] = ACompanyname
            item['CompanyID'] = ACompanyID
            item['CompanyId'] = CompanyId
            item['CompanyName'] = CompanyName
            item['Num'] = Num
            item['CompanyType'] = CompanyType
            item['Creat_time'] = self.starttime
            item['source'] = COMPANY_FROM
            item['sqltype'] = '2'
            yield item


    def analysis_page(self, response):
        item = YienmovieItem()
        response_page = json.loads(response.text)
        # print(response_page)
        Cinemasdata = response_page['Data']['Table1']
        Companyname = response.meta['Companyname']
        CompanyID = response.meta['CompanyID']
        for Cinemas in Cinemasdata:
            CinemaID = Cinemas['CinemaID']  # 影院id
            CinemaName = Cinemas['CinemaName']  # 影院名称
            Province = Cinemas['Province']  # 省份
            City = Cinemas['City']  # 城市
            Area = Cinemas['Area']  # 地区
            OnlineDate = Cinemas['OnlineDate']  # 开业时间
            Screen = Cinemas['Screen']  # 银幕数
            ScreenD = Cinemas['ScreenD']  # 3D银幕
            ScreenS = Cinemas['ScreenS']  # 数字
            Seat = Cinemas['Seat']  # 座位
            Tel = Cinemas['Tel']  # 电话

            item['Companyname'] = Companyname
            item['CompanyID'] = CompanyID
            item['CinemaID'] = CinemaID
            item['CinemaName'] = CinemaName
            item['Province'] = Province
            item['City'] = City
            item['Area'] = Area
            item['OnlineDate'] = OnlineDate
            item['Screen'] = Screen
            item['ScreenD'] = ScreenD
            item['ScreenS'] = ScreenS
            item['Seat'] = Seat
            item['Tel'] = Tel
            item['Creat_time'] = self.starttime
            item['source'] = COMPANY_FROM
            item['sqltype'] = '1'
            yield item


