import mysql.connector
from database import config
import redis
from redis import Redis, ConnectionPool
from datetime import datetime, timedelta, date
import time
import sys

def mysql_updater():

    db = mysql.connector.connect(**config)
    cursor = db.cursor()


    del_time = date.today()- timedelta(days=30)

    cursor.execute(
        f"""
        select gid, createtime from news_recommend.news_ago where createtime < "{del_time}"
    
        """)

    gid_del = [x[0] for x in cursor.fetchall()]  # 30일 전의 gid

    pool = ConnectionPool(host='localhost', port=6379, db=0)
    r = redis.Redis(connection_pool=pool)

    r_before = r.dbsize()
    if len(gid_del) > 0:
        r.delete(*gid_del)
    r_after = r.dbsize()


    cursor.execute("""
    select count(*), max(createtime), min(createtime) from news_recommend.news_ago
    """)
    count0, max0, min0 =  cursor.fetchone()
    m_before = count0
    max_before = max0.strftime('%Y-%m-%d %H:%M:%S')
    min_before = min0.strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute(
        f"""
        delete from news_recommend.news_ago where createtime < "{del_time}"
    
        """)
    db.commit()

    cursor.execute("""
    select count(*), max(createtime), min(createtime) from news_recommend.news_ago
    """)
    count0, max0, min0 =  cursor.fetchone()

    m_after = count0
    max_after = max0.strftime('%Y-%m-%d %H:%M:%S')
    min_after = min0.strftime('%Y-%m-%d %H:%M:%S')

    return len(gid_del), r_before, r_after, m_before, m_after, min_before, max_before, min_after, max_after

if __name__ == "__main__":
    last_update = datetime.now() - timedelta(days=1)
    while True:
        now0 = datetime.now()
        # print(last_update.date())
        # print(now0.date())
        if last_update.date() < now0.date():

            len_gid_del, r_before, r_after, m_before, m_after, min_before, max_before, min_after, max_after = mysql_updater()
            now0 = datetime.now()
            print(f"업데이트시간 : {datetime.now()}")
            print(f"삭제목록 : {len_gid_del}")
            print(f"redis size : {r_before} -> {r_after} / {r_before - r_after} 삭제")
            print(f"mysql size : {m_before} -> {m_after} / {m_before - m_after} 삭제")
            print(f"mysql : {min_before} ~ {max_before}  -> {min_after} ~ {max_after}")
            last_update = now0
            print("=================")
        print(f'현재시간 : {now0}', end='||')
        sys.stdout.flush()
        time.sleep(60*30)