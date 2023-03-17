from database import config
import mysql.connector
db = mysql.connector.connect(**config)
cursor = db.cursor()
#
# cursor.execute(
#     """
# SELECT table_schema AS "Database", SUM(data_length + index_length) / 1024 / 1024  AS "Size (MB)" FROM information_schema.TABLES GROUP BY table_schema
# """
# )
# print(cursor.fetchall())
#
#
#
# cursor.execute(
#     """
# SHOW columns FROM news_recommend.news_ago;
# """
# )
# print(cursor.fetchall())
#
cursor.execute(
    """
SHOW TABLE STATUS FROM news_recommend WHERE Name='news_ago';
"""
)
val = cursor.fetchall()[0]
column = [i[0] for i in cursor.description]
for i, c in enumerate(column):
    print(f"{c} :  {val[i]}")

print((val[6] + val[8] )/1024/1024)


cursor.execute(
    """
select length(test) from news_recommend.news_ago;
"""
)
print(cursor.fetchall()[0][0]/1024/1024)