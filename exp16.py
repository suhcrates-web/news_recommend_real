from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import gensim
import gensim.downloader as api

from database import cursor, db
import codecs
from konlpy.tag import Kkma, Komoran, Okt
import numpy as np
from collections import Counter
from gensim.test.utils import get_tmpfile
#
# okt = Okt()
# # kkm = Kkma()
# # kom = Komoran()
#
# cursor.execute(
#     """
#     select content from news_recommend.news_ago
#     """
# )
#
# results = cursor.fetchall()
# temp =[codecs.decode(i[0], 'utf-8') for i in results[: round(len(results)*2/3) ]]
# all_sample =[[i[:-5] for i in okt.pos(sample_list, norm=True, join=True) if i[-4:] =='Noun'] for sample_list in temp]
#
#
# def tagged_document(list_of_list_of_words):  # 리스트 형태로 넣어야함
#     for i, list_of_words in enumerate(list_of_list_of_words):
#         yield gensim.models.doc2vec.TaggedDocument(list_of_words, [i])
#
# data_for_training = list(tagged_document(all_sample))

vector_size = 50

model = gensim.models.doc2vec.Doc2Vec(vector_size=vector_size, min_count=2, epochs=40)
# model.layer1_size = 100
print(model.docvecs)
print()
print(model.corpus_count)
print(model.layer1_size)
# min_count :  n 개 이하로 나타난 단어는 지워버림.
# model.build_vocab(data_for_training)
# model.train(data_for_training, total_examples = model.corpus_count, epochs = model.epochs)
#
# model.save('test1.model')
# model.save('test.model')