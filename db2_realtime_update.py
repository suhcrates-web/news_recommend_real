#### db2 업데이트
import redis
from redis import Redis, ConnectionPool
import numpy as np
import json
import mysql.connector
from database import config
import time
import sys
from datetime import datetime, timedelta

pool = ConnectionPool(host='localhost', port=6379, db=0)
pool2 = ConnectionPool(host='localhost', port=6379, db=2)
pool3 = ConnectionPool(host='localhost', port=6379, db=3)

r = redis.Redis(connection_pool=pool)
r2 = redis.Redis(connection_pool=pool2)
r3 = redis.Redis(connection_pool=pool3)

def db2_updater():
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    vectors = []
    gid_list = []
    title_list = []
    url_list = []
    thumburl_list = []
    ## 동아
    cursor.execute(
        f"""
        select gid, title, url, thumburl from news_recommend.news_ago where source='동아일보' order by createtime desc limit 1300;
        """
    )

    for i, (gid, title, url, thumburl) in enumerate(cursor.fetchall()):
        vectors.append(np.frombuffer(r.get(gid), dtype='float32'))
        gid_list.append(gid)
        title_list.append(title)
        url_list.append(url)
        thumburl_list.append(thumburl)

    ## 다른 언론사
    cursor.execute(
        f"""
        select gid, title, url, thumburl from news_recommend.news_ago where source!='동아일보' order by createtime desc limit 700;
        """
    )

    for i, (gid, title, url, thumburl) in enumerate(cursor.fetchall()):
        vectors.append(np.frombuffer(r.get(gid), dtype='float32'))
        gid_list.append(gid)
        title_list.append(title)
        url_list.append(url)
        thumburl_list.append(thumburl)

    mat_b = np.array(vectors)
    r2.flushdb()
    r2.set('mat', mat_b.tobytes())
    r2.set('gid2', json.dumps(gid_list))
    r2.set('title', json.dumps(title_list))
    r2.set('url', json.dumps(url_list))
    r2.set('thumburl', json.dumps(thumburl_list))
    r2.set('temp', np.random.rand(50).astype('float32').tobytes()) # ***** 수정해야함

def db3_updater():
    ##### db3 update 도 같이 해줌. 60분이 지난 r3 키를 지워주는 역할.
    r3key = r3.keys('*')
    for time0 in r3key:
        if datetime.strptime(time0.decode('utf-8') + '0', "%Y%m%d%H:%M") < datetime.now() - timedelta(hours=1):
            r3.delete(time0)
    return len(r3key)

if __name__ == '__main__':
    time.sleep(60)
    n=0
    while True:
        n+=1
        now0 = datetime.now()
        db2_updater()
        if n%3 ==0:
            r3key = db3_updater()
            n=0
            print(f"업데이트 : {now0} / r3 key 수 : {r3key}") # 6개 내외로 유지돼야 함.
        else:
            print(f"업데이트 : {now0}")
        sys.stdout.flush()
        time.sleep(60*4)
