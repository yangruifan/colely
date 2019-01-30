import requests
import json
import time
from bs4 import BeautifulSoup

# datas = {
#     # 'huxiu_hash_code': '004ea0b8149a48eedea6937acfef59f5',
#     'page': '2',
#     # 'last_dateline': 1547258160,
# }
# header = {
#     'Referer': 'https://www.huxiu.com/',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, \
#     like Gecko)Chrome/68.0.3440.106 Safari/537.36'
# }
# response = requests.post(url='https://www.huxiu.com/v2_action/article_list', data=datas, headers=header)
# # print(response.text)
# response_page = json.loads(response.text)
# print(response_page['last_dateline'])
# response_page = response_page['data']
# # print(response_page)
#
# soup = BeautifulSoup(str(response_page), 'lxml')
# url = [i.find('a', class_='transition')['href'] for i in soup.find_all('div', class_='mod-b mod-art')]
# print(url)

from urllib import parse
import requests
from fake_useragent import UserAgent
from


class http_requests():
    def __init__(self, url=None, way='get', UA=False, **kwargs):
        self.url = url
        self.way = way
        self.data = {**kwargs}
        self.UA = UA

    def http_page(self):
        def requests_post(url=None, data=None, **kwargs):
            """
            用于请求get请求。
            :param url:
            :param kwargs:
            :return:
            """
            header = {'User-Agent': 'python'}
            # header['Referer'] = 'https://www.huxiu.com/'
            if {**kwargs}['UserAgent']:
                ua = UserAgent(verify_ssl=False)
                HEADERS['UserAgent'] = ua.random
            print(HEADERS)
            print(data)
            response = requests.post(url=url, data=data, headers=HEADERS)
            return response

        def requests_get(url=None, **kwargs):
            """
            用于请求get请求。
            :param url:
            :param kwargs:
            :return:
            """
            header = {'User-Agent': 'python'}
            if {**kwargs}['UserAgent']:
                ua = UserAgent(verify_ssl=False)
                header['UserAgent'] = ua.random
            print(header)
            response = requests.get(url=url, headers=header)
            print(url)
            return response

        if self.way == "get":
            data = parse.urlencode(self.data)
            url = self.url + "?" + data
            response = requests_get(url=url, UserAgent=self.UA)
        elif self.way == "post":
            response = requests_post(url=self.url, data=self.data, UserAgent=self.UA)
        else:
            response = None
        return response


if __name__ == '__main__':
    a = http_requests(url='http://www.baidu.com/s', way='get', wd='你好')
    response = a.http_page()
    print(response.text)
