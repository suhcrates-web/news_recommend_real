from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import gensim
import redis
from konlpy.tag import Okt
from database import db, cursor
import codecs
import numpy as np

### db=0  (기사 gid:벡터  환경 만들기. 30일치 긁어와서.)

okt = Okt()
r = redis.Redis(host='localhost', port=6379)
model = Doc2Vec.load('test.model')
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

for gid, content in ar_dic.items():
    jogaked = jogakjogak(codecs.decode(content, 'utf-8'))
    jogaked = model.infer_vector(jogaked)
    # r.set(gid, str(jogaked))

    # a=np.array(jogaked)
    # a =np.fromstring(a, dtype='float32') ## 요거 안써주면 이상해짐
    r.set(gid, np.array(jogaked).tostring())  # tostring() 기반.
    print(gid)
