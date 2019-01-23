"""{
"name": "mdjfk",
"index_to_monitor": 10,
"last_index": 30,
"first_finished": false,
"page_size": 17,
"page_index_step": 1,
"create_time": "2019-01-07 03:08:21",
"extract_list_rule": "//article/a/@href",
"extract_title_rule": "//h1[1]/text()",
"extract_content_rule": "//div[@class='body']",
"ad_rule": "not set",
"root_url": "http://www.shift.jp.org",
"is_active": true,
"url_template": "http://www.shift.jp.org/cn/blog/page/{}/",
"exists_list": false,
"extract_author_rule":"作者提取规则",
"extract_crtime_rule":"文章发表时间提取规则"
}"""
import requests
import datetime
import json

"""xpath规则中全用单引号"""

datas = {
    "id": 2,
    "name": "光明日报",
    # 网站名称
    "index_to_monitor": 3,
    # 每天检查的文章数量
    "last_index": 10,
    # 有多少页列表
    "first_finished": 0,
    # 是否一次爬完全站，没有0，有1
    "page_size": 50,
    # 一个文件列表有多少条文章
    "page_index_step": 1,
    # 步长
    "create_time": "",
    # 源创建的时间
    "extract_list_rule": "//div[@class='channelLeftPart']/div/ul/li/span/a/@href",
    # 列表页的提取规则
    "extract_title_rule": "//h1[@class='u-title']/text()",
    # 文章标题的提取规则
    "extract_content_rule": "//div[@id='articleBox']",
    # 内容的提取规则
    "extract_author_rule": "//span[@class='m-con-source']/a/text()",
    # 作者提取规则
    "extract_crtime_rule": "//span[@class='m-con-time']/text()",
    # 文章发表时间提取规则
    "ad_rule": "not set",
    # 从文章列表页面抽出广告的规则
    "root_url": "http://news.gmw.cn/node_4108.htm",
    # 根url
    "is_active": 1,
    # 是否启用源
    "url_template": "http://news.gmw.cn/node_4108_{}.htm",
    # 生成列表URL的模板字符串
    "exists_list": 1,
    # 是否存在列表页
}

url = "http://10.125.0.8:12310/api/v1/sourceSave"
datas['create_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
datas = json.dumps(datas)
response = requests.post(url=url,
                         data=datas,
                         )
print(response)
print(response.text)
