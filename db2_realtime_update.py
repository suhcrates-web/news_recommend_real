#### db2 업데이트
import redis
from redis import Redis, ConnectionPool
import numpy as np
import json
import mysql.connector
from database import config
import time


pool = ConnectionPool(host='localhost', port=6379, db=0)
pool2 = ConnectionPool(host='localhost', port=6379, db=2)

r = redis.Redis(connection_pool=pool)
r2 = redis.Redis(connection_pool=pool2)
def db2_updater():
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

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
        mat[i:] =np.frombuffer(r.get(gid), dtype='float32')
        gid_list.append(gid)

        title_list.append(title)
        url_list.append(url)
        thumburl_list.append(thumburl)

    mat_b = mat.tobytes()

    r2.flushdb()
    r2.set('mat', mat_b)
    r2.set('gid2', json.dumps(gid_list))
    r2.set('title', json.dumps(title_list))
    r2.set('url', json.dumps(url_list))
    r2.set('thumburl', json.dumps(thumburl_list))

if __name__ == '__main__':
    n=1
    while True:
        db2_updater()
        print(f"{n} 사이클 완료")
        n += 1
        print("==============")
        time.sleep(120)
