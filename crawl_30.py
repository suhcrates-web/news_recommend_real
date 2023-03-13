import requests
import json
from database import  config
import mysql.connector
from datetime import date, timedelta
import binascii
import re

today0 = date.today()
for i in range(29):
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    print(f"날짜:{i}")
    day0 = today0 - timedelta(days=i)
    url = f'https://openapi.donga.com/newsList?p={day0.strftime("%Y%m%d")}'
    temp = requests.get(url)
    articles = json.loads(temp.content)['data']
    n=0

    for ar in articles:
        n+=1
        print(f"{i}   {n}")

        content = ar["content"]
        title = ar['title']
        if len(content)>400 and '[부고]' not in title and '[인사]' not in title and '[단신]' not in title:
            # print(ar['title'])
            # print(ar['url'])
            content0 =content
            # content = re.sub(r'[^\s]+@.+\..+', ' ',  content)
            content = re.sub(r'[^\s]+@[a-zA-Z.]+', ' ',  content)
            content = re.sub(r'[!?.][^.]*$', '.', content)
            # print(ar['url'])
            # print([content0[len(content):]])
            title = ar['title'].replace('"','“')
            # print("=================================")

            cursor.execute(
                f"""
                insert into news_recommend.news_ago values(
                "{ar['gid']}", "{ar['createtime']}", "{title}", b'{bin(int(binascii.hexlify(content.encode("utf-8")), 16))[2:]}', "{ar['url']}", "{ar['thumburl']}","{ar['source']}",NULL)
                """
            )
            # print("=================================")
            # print("=================================")
    db.commit()
# db.commit()