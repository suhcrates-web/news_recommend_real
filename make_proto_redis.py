from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import gensim
import redis
from konlpy.tag import Okt
import mysql.connector
from database import config
import codecs
import numpy as np
import binascii
import json

db = mysql.connector.connect(**config)
cursor = db.cursor()

### db=0  (기사 gid:벡터  환경 만들기. 30일치 긁어와서.)
okt = Okt()
r = redis.Redis(host='localhost', port=6379)
model = Doc2Vec.load('donga2000.model')
r.flushdb()

cursor.execute(
    """
    select gid, content from news_recommend.news_ago
    """
)

ar_dic = {k:v for k,v in cursor.fetchall()}

for gid, content in ar_dic.items():
    konlpy0 = okt.pos(codecs.decode(content, 'utf-8'), norm=True, join=True)
    vector0 = model.infer_vector(konlpy0)
    vector0 = np.array(np.array(vector0))
    r.set(gid, vector0.tobytes())  # tobytes() 기반.
    print(gid)
    cursor.execute(
        f"""
        update news_recommend.news_ago set vec= b'{bin(int(binascii.hexlify(str(list(vector0)).encode("utf-8")), 16))[2:]}', konlpy =b'{bin(int(binascii.hexlify(str(json.dumps(konlpy0)).encode("utf-8")), 16))[2:]}' where gid='{gid}'
        """
    )
db.commit()
