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
import make_test_user_db
p = 0.3
time0 = []
time1 = []
result0 = []
result1 = []
for _ in range(2000):
    gid = test_ga[np.random.randint(0, len(test_ga))]
    ga = gid

    # g_vec = np.array(json.loads(r.get(gid)))  # 기사벡터
    # u_vec = np.array(json.loads(r1.get(ga)))  # 유저벡터
    g_vec = np.fromstring(r.get(gid), dtype='float32')
    u_vec = np.fromstring(r1.get(ga), dtype='float32')

    u_vec = (1-p) * g_vec + p * u_vec
    # r1.set(ga,str(list(u_vec)))
    mat = r2.get('mat')
    mat = np.fromstring(mat).reshape(700, 50)

    top10 = list(find_10_alt(mat,u_vec))

    #1) mysql 방식
    start = timeit.default_timer()
    gid_list = json.loads(r2.get('gid2'))
    result1 = [gid_list[x] for x in top10]
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    cursor.execute(
        f"""
        select title, url, thumburl from news_recommend.news_ago where gid in ({','.join(result1)})
        """
    )
    dics0 = {}
    for i, (title,url,thumburl) in enumerate(cursor.fetchall()):
        dics0[i] = {'title':title, 'url':url, 'thumburl':thumburl}
    end = timeit.default_timer()
    time0.append(end-start)

    #2) redis - json   : mysql 보다 4~5배 빠름
    start = timeit.default_timer()
    title_list = json.loads(r2.get('title'))
    url_list = json.loads(r2.get('url'))
    thumburl_list = json.loads(r2.get('thumburl'))
    result1 = [gid_list[x] for x in top10]
    dics1 = {}
    for i, x in enumerate(top10):
        dics1[i] = {'title':title_list[x], 'url':url_list[x], 'thumburl':thumburl_list[x]}
    end = timeit.default_timer()
    time1.append(end-start)

print(dics0)
print("==============")
print(dics1)
print("==============")
print(max(time0))
print(min(time0))
print(np.mean(time0))
print(sum(time0))
print("==============")
print(max(time1))
print(min(time1))
print(np.mean(time1))
print(sum(time1))

# 0.007391500024823472
# 0.0032353999849874526
# 0.00377636010000424
# 7.55272020000848

# 0.047407800011569634
# 0.0029451999871525913
# 0.008297619900127756
# 16.595239800255513
# r.quit()