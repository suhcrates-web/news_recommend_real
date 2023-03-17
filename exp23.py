import requests
import json
import mysql.connector
from database import config
from datetime import date, timedelta, datetime
import binascii
import re
import redis
from redis import Redis, ConnectionPool
from gensim.models.doc2vec import Doc2Vec
from konlpy.tag import Okt
import numpy as np
import time
import gc
import sys

articles = []
api_dic = {}
today0 = date.today()
for n in range(1):  # 수정, 삭제는 이틀치를 확인해야 하기떄문에 이틀치 긁어옴.
    day0 = today0 - timedelta(days=n)  # 어제(n=1), 오늘(n=0)
    url = f'https://openapi.donga.com/newsList?p={day0.strftime("%Y%m%d")}'
    temp = requests.get(url)
    articles += json.loads(temp.content)['data']
for ar in articles:
    print(f"{ar['title']}  / {ar['gid']}")
