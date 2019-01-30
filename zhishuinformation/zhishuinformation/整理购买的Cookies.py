import re
import json
import redis


def redis_push(data):
    r = redis.Redis(host='10.125.0.7', port=6379, db=0, password='crs-hbnwcb9i:r@16samVW!jh',socket_connect_timeout=5)
    #redis.Redis(host='10.125.0.7', port=6379, db=0, password='crs-hbnwcb9i:r@16samVW!jh',socket_connect_timeout=5)
    # r = redis.Redis(host='127.0.0.1', port=6379, db=0)
    data = {
        'name': 'BDUSS',
        'value': data,
    }
    json_data = json.dumps(data)
    r.lpush('baiduCookies', json_data)


with open('./information.txt', encoding="gbk", errors='ignore') as f:
    data = f.read()

reg = r"'*?BDUSS=(.*?);.*?"
infor = re.findall(reg, data, re.S)
print(len(infor))

for i in infor:
    redis_push(i)

# rpoplpush(src, dst)
# 从一个列表取出最右边的元素，同时将其添加至另一个列表的最左边
# src 要取数据的列表
# dst 要添加数据的列表

# r = redis.Redis(host='10.125.0.7', port=6379, db=0, password='crs-hbnwcb9i:r@16samVW!jh',socket_connect_timeout=5)
#redis.Redis(host='10.125.0.7', port=6379, db=0, password='crs-hbnwcb9i:r@16samVW!jh',socket_connect_timeout=5)
# r = redis.Redis(host='127.0.0.1', port=6379, db=0)
# data = r.rpoplpush('baiduCookiess', 'baiduCookiess')
# print(data)
# data = r.rpoplpush('baiduCookiess', 'baiduCookiess')
# print(data)

