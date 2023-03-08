## list  를 redis 에 json 파싱해 넣는게 빠른지  rpush 로 넣는게 빠른지 실험.
#json 파싱이 빠름


import redis
import numpy as np
import redis
import json
import timeit
from database import db, cursor

r = redis.Redis(host='localhost', port=6379)
ran_ma = np.random.rand(100)
r.flushdb()

number0 = 1000
#1) json으로.  이게 더 나은 방법
## 이게 3번보다 10배 빠름. 2번보다 3배 빠름
# 인출횟수가 많아질땐 1번은 속도가 그대로고 2번은 급격히 느려짐
# 인출횟수가 1000번에 이르면 2번은 거의 무용지물. 1이 제일 빠르고 안정적.

list1 =[]
for _ in range(number0):
    start = timeit.default_timer()
    r.set('json',str(list(ran_ma)))
    val = r.get('json')
    temp= json.loads(val)
    # print(temp)
    end = timeit.default_timer()
    time1 = end-start
    list1.append(time1)
print(max(list1))
print(min(list1))
print(np.mean(list1))
print("========================")

#2) rpush 로 내부 list에 저장.
r.flushdb()
list1 =[]
for _ in range(number0):
    start = timeit.default_timer()
    r.rpush('list', *list(ran_ma))
    temp = r.lrange('list',0,-1)
    temp = [float(elem.decode('utf-8')) for elem in temp]
    # print(temp)
    end = timeit.default_timer()
    time2= end-start
    list1.append(time2)
print(max(list1))
print(min(list1))
print(np.mean(list1))
print("========================")
#3) mysql로 저장. 이게 2번보다 2배 빠르고 1번보다 2배 느림
# 근데 저장하는 데이터 길이가 짧아질수록 1,2번의 속도가 급속히 짧아지는 반면 3번의 속도는 그대로임

list1 =[]
cursor.execute(
        f"""
        truncate news_recommend.test
        """
    )
for _ in range(number0):
    start = timeit.default_timer()
    cursor.execute(
        f"""
        insert into news_recommend.test values('{str(list(ran_ma))}','{_}')
        """
    )
    db.commit()
    cursor.execute(
        f"""
        select test from news_recommend.test where id='{_}'
        """
    )
    json.loads(cursor.fetchone()[0])
    end = timeit.default_timer()
    time3= end-start
    list1.append(time3)
print(max(list1))
print(min(list1))
print(np.mean(list1))
print("========================")
print(time1)
print(time2)
print(time3)
# print(ran_ma)
# r = redis.Redis(host='localhost', port=6379)
#
# r.flushdb()
# r.