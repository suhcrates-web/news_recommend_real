import requests
import json
from database import db, cursor
from datetime import date, timedelta
import binascii
import re

today0 = date.today()
for i in range(30):
    print(f"날짜:{i}")
    day0 = today0 - timedelta(days=i)
    url = f'https://openapi.donga.com/newsList?p={day0.strftime("%Y%m%d")}'
    temp = requests.get(url)
    articles = json.loads(temp.content)['data']
    n=0

    for ar in articles:
        print(ar)
        n+=1
        print(f"{i}   {n}")

        content = ar["content"]
        if len(content)>400:
            # print(ar['title'])
            # print(ar['url'])
            print(content)
            content = re.split(r'[^\s]+@.+\..+',  content)
            print(content)
            content = re.sub(r'\.[^.]*$', '.', content)
            title = ar['title'].replace('"','“')
            # print("=================================")
            # print(content)
            cursor.execute(
                f"""
                insert into news_recommend.news_ago values(
                "{ar['gid']}", "{ar['createtime']}", "{title}", b'{bin(int(binascii.hexlify(content.encode("utf-8")), 16))[2:]}', "{ar['url']}", "{ar['thumburl']}")
                """
            )
            # print("=================================")
            # print("=================================")
    # db.commit()
# db.commit()