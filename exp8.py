### 제일 빨리 업로드된 순으로 700개 인출, 정리하는 작업
### mat 만들어서 저장 및 인출
### title, url 등도 꺼내서
### redis 서버2 에 넣는 작업

from pymemcache.client import base
import redis
import numpy as np
import timeit
from database import db, cursor
import json

# mat = np.random.rand(700,50)
# print(mat)

r = redis.Redis(host='localhost', port=6379, db=0)

num_gisa = 700
cursor.execute(
    f"""
    select gid, title, url, thumburl from news_recommend.news_ago order by createtime desc limit {num_gisa}
    """
)

mat = np.zeros((num_gisa,50))
gid_list = []
title_list = []
url_list = []
thumburl_list = []

for i, (gid, title, url, thumburl) in enumerate(cursor.fetchall()):
    mat[i:] =np.fromstring(r.get(gid), dtype='float32')
    gid_list.append(gid)

    title_list.append(title)
    url_list.append(url)
    thumburl_list.append(thumburl)

mat_b = mat.tostring()
r2 = redis.Redis(host='localhost', port=6379, db=2)
r2.flushdb()
# ## memecached
# client.set('mat', mat_b)
# mat_m = client.get('mat')
# print(np.fromstring(mat_m))

## redis.
# memcached는 그냥 안쓰기로. 윈도에서 테스트할 수 없음.
# mysql 보다 redis 가 확실히 안정적이고 빠름.

r2.set('mat', mat_b)

#gid 목록
#v1
r2.rpush('gid1', *gid_list)
r2.set('gid2', json.dumps(gid_list))
r2.set('title', json.dumps(title_list))
r2.set('url', json.dumps(url_list))
r2.set('thumburl', json.dumps(thumburl_list))
exit()
time0 = []
for _ in range(10000):
    start = timeit.default_timer()
    mat_r = r2.get('mat')
    mat_r = np.fromstring(mat_r, )
    mat_r = mat_r.reshape(700,50)
    end = timeit.default_timer()
    time0.append(end-start)

print(max(time0))
print(min(time0))
print(np.mean(time0))