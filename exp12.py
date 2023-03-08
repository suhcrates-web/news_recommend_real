### 삭제 수정 뼈대


import requests
import json
from datetime import date, timedelta
import mysql.connector

today0 = date.today()
print(today0)

articles = []
api_dic = {}
for n in range(2):
    day0 = today0 - timedelta(days=n)
    url = f'https://openapi.donga.com/newsList?p={day0.strftime("%Y%m%d")}'
    temp = requests.get(url)
    articles +=json.loads(temp.content)['data']
for ar in articles:
    api_dic[ar['gid']] = ar['title']


config = {
    'user' : 'root',
    'password': 'Seoseoseo7!',
    'host':'localhost',
    # 'database':'shit',
    'port':'3306'
}

db = mysql.connector.connect(**config)
cursor = db.cursor()

cursor.execute(
    f"""
    select gid, title, createtime from news_recommend.news_ago where createtime >="{today0 - timedelta(days=1)}" and createtime < "{today0 + timedelta(days=1)}" 
    """
)

mysql_dic = {g:(t,c) for g,t, c in cursor.fetchall()}  # gid : title

# mysql 에 있는 것 중 api 에 없는것을 찾아야 함
for gid in mysql_dic:
    print(mysql_dic[gid][1], end=' ')
    if gid not in [*api_dic]:
        print("삭제해야됨")
    elif api_dic[gid] != mysql_dic[gid][0] : # gid가 있긴 한데 title이 다를 경우
        print(f"{api_dic[gid]} / {mysql_dic[gid][0]} ")
        print("수정해야됨")
    else:
        print("이상없음")
