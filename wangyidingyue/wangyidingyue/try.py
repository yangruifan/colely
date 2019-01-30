# import requests
# import json
# url = 'http://dy.163.com/v2/article/list.do?pageNo=1&wemediaId=W8032893525454075161&size=1'
# response = requests.get(url)
# data = json.loads(response.text)
# data = data['data']['list'][0]
# print(data)
import time
# 字符类型的时间
tss1 = '2018-12-24'
# 转为时间数组
timeArray = time.strptime(tss1, "%Y-%m-%d")
print(timeArray)
# 转为时间戳
timeStamp = int(time.mktime(timeArray))
print (timeStamp  ) # 1381419600