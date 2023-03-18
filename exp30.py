from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import gensim
import gensim.downloader as api
import mysql.connector
from database import config
import codecs

db = mysql.connector.connect(**config)
cursor = db.cursor()


cursor.execute(
    """
    select content, url from news_recommend.news_ago where source = "동아일보" order by createtime desc
    """
)

results = cursor.fetchall()
for i, url in results:
    temp = codecs.decode(i, 'utf-8')
    print(temp)

    print(url)
    print(len(temp))
    input("ok?")
    print("###############################################")