import time
from datetime import date, timedelta
import mysql.connector
from database import config
db = mysql.connector.connect(**config)
cursor = db.cursor()

del_time = date.today() - timedelta(days=30)

cursor.execute(
    f"""
        select gid, createtime from news_recommend.news_ago where createtime < "{del_time}"

        """)

gid_del = [x[0] for x in cursor.fetchall()]
print(gid_del)