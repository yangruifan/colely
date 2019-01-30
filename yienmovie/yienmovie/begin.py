from scrapy import cmdline
cmdline.execute('scrapy crawl spider'.split())
#
# import requests
# import datetime
# import json
#
# class get_Cinema_from_Company():
#     def __init__(self):
#         self.header = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
#             (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
#             }
#         starttime = datetime.date.today()
#         endtime = starttime-datetime.timedelta(days=365)
#         self.starttime = starttime
#         self.endtime = endtime
#
#     def get_Company_ID_NAME(self):
#         url = 'http://ebotapp.entgroup.cn/API/DataBox/Company/CompanyBoxOfficeByDate'
#         data = {
#             # 'r': '0.36080874899985793',
#             'PageIndex': '1',
#             'PageSize': '1000',
#             'Order': '201',
#             'OrderType': 'DESC',
#             'Index': '101,102,201,203,604',
#             'ServicePrice': '1',
#             'DateSort': 'Day',
#             'Date': self.starttime,
#             'sDate': self.starttime,
#             'eDate': self.starttime,
#         }
#         response = requests.post(url=url, data=data, headers=self.header)
#         response_page = json.loads(response.text)
#         Companydatas = response_page['Data']['Table2']
#         self.Companys = {}
#         for Company in Companydatas:
#             self.Companys[Company['CompanyID']] = Company['CompanyName']
#         # print(self.Companys)
#
#     def get_Cinema(self):
#         url = 'http://ebotapp.entgroup.cn/API/DataBox/Company/CompanyInvestCinema'
#         for key, value in self.Companys.items():
#             print(key, value)
#             data = {
#                 # 'r': '0.06027488414856186',
#                 'Company': str(key),
#                 'PageIndex': '1',
#                 'PageSize': '500',
#                 'DateSort': 'Self',
#                 # 'Date': '2018-10-16,2019-01-16',
#                 'sDate': self.endtime,
#                 'eDate': self.starttime,
#             }
#             response = requests.post(url=url, data=data, headers=self.header)
#             print(response.text)
#
# if __name__ == '__main__':
#     data = get_Cinema_from_Company()
#     data.get_Company_ID_NAME()
#     data.get_Cinema()