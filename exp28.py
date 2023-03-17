from konlpy.tag import Okt
from database import config
import mysql.connector
import codecs
import ast
import binascii
import json
db = mysql.connector.connect(**config)
cursor = db.cursor()
okt = Okt()
#
cursor.execute(
    """
    select gid, content from news_recommend.news_ago
    """
)

for gid, content in cursor.fetchall()[:1]:
    # content = codecs.decode(content, 'utf-8')
    # temp= okt.pos(content, norm=True, join=True)
    temp = ['a','"asdf"','123""']
    cursor.execute(
        f"""
        update news_recommend.test set test123123=b'{bin(int(binascii.hexlify(str( json.dumps(temp) ).encode("utf-8")), 16))[2:]}' where id='0'
        """
    )
db.commit()

# # # #df
cursor.execute("""
select test123123 from news_recommend.test where id='0'
""")
print(json.loads(codecs.decode(cursor.fetchall()[0][0], 'utf-8'))[1])
