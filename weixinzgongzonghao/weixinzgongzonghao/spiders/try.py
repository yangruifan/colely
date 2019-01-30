import redis
r= redis.Redis(host='127.0.0.1',port=6379,decode_responses=True)
r.hmset('hashmore',{'k1':'v1','k2':'v2','k3':'v3'})
print(r.hmget('hashmore','k1','k2','k3'))
print(r.hgetall('hashmore'))