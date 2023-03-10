import redis
from redis import Redis, ConnectionPool
from database import cursor, db
import numpy as np
import binascii
import json
pool = ConnectionPool(host='localhost', port=6379, db=0)
pool1 = ConnectionPool(host='localhost', port=6379, db=1)
pool2 = ConnectionPool(host='localhost', port=6379, db=2)
r = redis.Redis(connection_pool=pool)
r1 = redis.Redis(connection_pool=pool1)
r2 = redis.Redis(connection_pool=pool2)


a = np.frombuffer(r.get('118138324'),dtype='float32')
#
print(a)
cursor.execute(
    f"""
    update news_recommend.test set test= b'{bin(int(binascii.hexlify(str(list(a)).encode("utf-8")), 16))[2:]}' where id=6
    """
)
db.commit()

cursor.execute(
    f"""
    select test from news_recommend.test where id=6
    """
)
print(np.array(json.loads(cursor.fetchall()[0][0])))

# print(np.frombuffer(cursor.fetchall()[0][0], dtype='float32'))