from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import gensim
import redis
from konlpy.tag import Okt
import mysql.connector
from database import config
import codecs
import numpy as np
import binascii

db = mysql.connector.connect(**config)
cursor = db.cursor()

### db=0  (기사 gid:벡터  환경 만들기. 30일치 긁어와서.)
okt = Okt()
r = redis.Redis(host='localhost', port=6379)
model = Doc2Vec.load('test1.model')
r.flushdb()
def tagged_document(list_of_list_of_words):  # 리스트 형태로 넣어야함
    for i, list_of_words in enumerate(list_of_list_of_words):
        yield gensim.models.doc2vec.TaggedDocument(list_of_words, [i])

def jogakjogak(text): #조각냄
    result = [i[:-5] for i in okt.pos(text, norm=True, join=True) if i[-4:] =='Noun']
    return result


cursor.execute(
    """
    select gid, content from news_recommend.news_ago
    """
)

ar_dic = {k:v for k,v in cursor.fetchall()}
print(ar_dic)
for gid, content in ar_dic.items():
    jogaked = jogakjogak(codecs.decode(content, 'utf-8'))
    jogaked = model.infer_vector(jogaked)
    jogaked = np.array(jogaked)
    r.set(gid, jogaked.tobytes())  # tobytes() 기반.
    print(gid)

    cursor.execute(
        f"""
        update news_recommend.news_ago set vec= b'{bin(int(binascii.hexlify(str(list(jogaked)).encode("utf-8")), 16))[2:]}' where gid='{gid}'
        """
    )
db.commit()
