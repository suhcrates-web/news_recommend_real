from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import gensim
import gensim.downloader as api
import mysql.connector
from database import config
import codecs
from konlpy.tag import Kkma, Komoran, Okt
import numpy as np
from collections import Counter
from gensim.test.utils import get_tmpfile

db = mysql.connector.connect(**config)
cursor = db.cursor()

okt = Okt()
# kkm = Kkma()
# kom = Komoran()

cursor.execute(
    """
    select content from news_recommend.news_ago where source="동아일보" and length > 1000 order by createtime desc limit 2000
    """
)

results = cursor.fetchall()
temp =[codecs.decode(i[0], 'utf-8') for i in results]
print("형태소 변환 중. 10분 소요")
all_sample =[okt.pos(sample_list, norm=True, join=True) for sample_list in temp]


def tagged_document(list_of_list_of_words):  # 리스트 형태로 넣어야함
    for i, list_of_words in enumerate(list_of_list_of_words):
        yield gensim.models.doc2vec.TaggedDocument(list_of_words, [i])

data_for_training = list(tagged_document(all_sample))

vector_size = 50
model = gensim.models.doc2vec.Doc2Vec(vector_size=vector_size, min_count=2, epochs=40)
# min_count :  n 개 이하로 나타난 단어는 지워버림.
model.build_vocab(data_for_training)
print("모델 트레이닝")
model.train(data_for_training, total_examples = model.corpus_count, epochs = model.epochs)

model.save('donga2000.model')
print("모델 생성 완료.  'donga2000.model' 저장")