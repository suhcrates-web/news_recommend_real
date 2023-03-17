#### OKT, 모델 로드, infer 속도 비교 ######



from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import gensim
from konlpy.tag import Kkma, Komoran, Okt
import mysql.connector
from database import config
import codecs
import timeit

db = mysql.connector.connect(**config)
cursor = db.cursor()


cursor.execute(
    """
    select content from news_recommend.model_test order by createtime limit 10
    """
)
okt = Okt()

temp = []


for con in cursor.fetchall():
    temp.append(codecs.decode(con[0], 'utf-8'))

start = timeit.default_timer()
all_sample = [okt.pos(sample_list, norm=True, join=True) for sample_list in temp]
end = timeit.default_timer()
print(end-start)

start = timeit.default_timer()
model = Doc2Vec.load(f'donga2000.model')
end = timeit.default_timer()
print(end-start)

start = timeit.default_timer()
for con in all_sample:
    vec =model.infer_vector(con)
end = timeit.default_timer()
print(end-start)


# OKT       2.6552770000052988
# 모델 load  0.12035489999834681
# infer     0.02565820000017993