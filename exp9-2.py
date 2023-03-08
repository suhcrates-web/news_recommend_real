## matrix 를 만들어  memcashed 에 넣기

# mysql 에서 최근 700개의 gid 꺼내오기
# gid에 해당하는 벡터를 redis에서 꺼내기
# matrix 쌓기
# memecashed에 저장.

#일단 memcashed에 뭔가 저장하는거부터 해보기

## 실험용 50*700 매트릭스는  redis db=2 에 key=mat 으로.

import numpy as np
import timeit
import json
import time
import redis
from redis import Redis, ConnectionPool
from collections import Counter
import mysql.connector

config = {
    'user' : 'root',
    'password': 'Seoseoseo7!',
    'host':'localhost',
    # 'database':'shit',
    'port':'3306'
}




test_ga = [117613119,117634894,117636851,117636957,117637748,117637908,117637911,117637913,117637915,117637916,117637917,117637922,117637923,117637924,117638121,117638182,117638235,117638241,117638243,117638357,117638362,117638539,117638807,117639038,117639044,117639048,117639051,117639068,117639071,117639074,117639090,117639280,118097360,118097514,118097796,118097905,118098139,118098178,118098301,118098414,118098440,118098539,118098701]

def find_10_alt(tot_mat, user_vector):
    points = np.matmul(tot_mat, user_vector)
    top10 = np.argsort(points)[::-1][:10]
    return top10


pool = ConnectionPool(host='localhost', port=6379, db=0)
pool1 = ConnectionPool(host='localhost', port=6379, db=1)
pool2 = ConnectionPool(host='localhost', port=6379, db=2)

r = redis.Redis(connection_pool=pool)
r1 = redis.Redis(connection_pool=pool1)
r2 = redis.Redis(connection_pool=pool2)


# r1 = redis.Redis(host='localhost', port=6379, db=1)
# r1.flushdb()
# import make_test_user_db
p = 0.3
time0 = []
time1 = []
result0 = []
result1 = []
for _ in range(1):
    gid = test_ga[np.random.randint(0, len(test_ga))]
    ga = gid
    start = timeit.default_timer()
    for _ in range(3):
        try:
            g_vec = np.fromstring(r.get(gid), dtype='float32')
            u_vec = np.fromstring(r1.get(ga), dtype='float32')
            u_vec = (1-p) * g_vec + p * u_vec
            r1.set(ga,u_vec.tostring())
            mat = r2.get('mat')
            mat = np.fromstring(mat).reshape(700, 50)
            top10 = list(find_10_alt(mat,u_vec))
            a = r2.get('title')
            title_list = json.loads(a)
            url_list = json.loads(r2.get('url'))
            thumburl_list = json.loads(r2.get('thumburl'))
            dics1 = {}
            for i, x in enumerate(top10):
                dics1[i] = {'title':title_list[x], 'url':url_list[x], 'thumburl':thumburl_list[x]}
            break
        except Exception as e:
            print(e)
    end = timeit.default_timer()
    time1.append(end - start)


print("==============")
print(dics1)
# print("==============")
# print(max(time0))
# print(min(time0))
# print(np.mean(time0))
# print(sum(time0))
print("==============")
print(max(time1))
print(min(time1))
print(np.mean(time1))
print(sum(time1))

