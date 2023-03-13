#### db 0 업데이트 작업
# 10초에 한번 api로 받아와, doc2vec 에 넣은 뒤  벡터 산출해 저장.
# api 정보는 mysql 에도 동시에 저장.

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


pool = ConnectionPool(host='localhost', port=6379, db=0)
r = redis.Redis(connection_pool=pool)

def updater(clean0):
    keys = [x.decode('utf-8') for x in r.keys('*')]  # redis db 0 에 저장된 key 값 (gid) 모두 인출.
    model = Doc2Vec.load('test1.model')  # doc2vec 모델 로드.
    okt = Okt()  # 형태소 변환 모듈

    today0 = date.today()

    articles = []
    api_dic = {}
    for n in range(2):  # 수정, 삭제는 이틀치를 확인해야 하기떄문에 이틀치 긁어옴.
        day0 = today0 - timedelta(days=n)  # 어제(n=1), 오늘(n=0)
        url = f'https://openapi.donga.com/newsList?p={day0.strftime("%Y%m%d")}'
        temp = requests.get(url)
        articles += json.loads(temp.content)['data']
    for ar in articles:
        api_dic[ar['gid']] = ar['title']   ### 제목 수정 에서 쓸  딕셔너리.

    ## 1) 새로 업데이트된 기사 정보를 mysql에 쌓음. 또 본문을 word2vec 으로 vec 변환해 redis에  'gid : vec' 형태로 저장함.
    def jogakjogak(text): #조각냄
        result = [i[:-5] for i in okt.pos(text, norm=True, join=True) if i[-4:] =='Noun']
        return result

    # def press_checker(text):
    #     result = 'unknown'
    #     if 'donga' in text:
    #         if '닷컴'in text :
    #             result = '동아닷컴'
    #         else:
    #             result = '동아'
    #     else:
    #         if '뉴시스' in text:
    #             result = '뉴시스'
    #         elif '뉴스1' in text:
    #             result = '뉴스1'
    #     return result

    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    # 작업을 수행하기 전 상태 체크
    cursor.execute("""
    select count(*), max(createtime), min(createtime) from news_recommend.news_ago
    """)
    before_count, before_max, before_min =  cursor.fetchone()

    num_recieve = len(articles)  # api로 받은 숫자
    num_deal = 0  # 실제 처리대상 숫자..  400자 이상,  부고 인사 단신 제외
    num_doc2vec = 0  # doc2vec 처리돼 redis와 mysql에 들어간 숫자.
    for ar in articles:
        content = ar["content"]
        if len(content) > 400:
            gid = ar['gid']
            if gid not in keys:  ## api에서 받은 게 redis 에 없다면
                num_deal += 1
                title = ar['title'].replace('"', '“')
                if '[부고]' not in title and '[인사]' not in title and '[단신]' not in title:
                    num_doc2vec +=1
                    if clean0:
                        print('\n============')
                        clean0 = False
                    print(f"기사 등록 : {gid} / {title} / {ar['url']}")
                    content = re.sub(r'\.com$','', content.strip())
                    temp = re.split(r'\.(?=[^.]*$)', content)
                    if len(temp) >1:
                        content, press = temp
                    else:
                        content, press = temp[0], 'unknown'

                    # doc2vec 변환 후 redis에 넣기
                    jogaked = jogakjogak(content)
                    jogaked = model.infer_vector(jogaked)
                    jogaked = np.array(np.array(jogaked))
                    r.set(gid, jogaked.tostring())
                    # mysql에 넣기
                    cursor.execute(
                        f"""
                        insert into news_recommend.news_ago values(
                        "{ar['gid']}", "{ar['createtime']}", "{title}", b'{bin(int(binascii.hexlify(content.encode("utf-8")), 16))[2:]}', "{ar['url']}", "{ar['thumburl']}", "{ar['source']}", b'{bin(int(binascii.hexlify(str(list(jogaked)).encode("utf-8")), 16))[2:]}')
                        """
                    )
                      # 벡터를 mysql에도 저장. 인출떄는  np.array(json.loads(cursor.fetchall()[0][0]))
    db.commit()

    # 2) 기사 수정 및 삭제

    cursor.execute(
        f"""
        select gid, title, createtime from news_recommend.news_ago where createtime >="{today0 - timedelta(days=1)}" and createtime < "{today0 + timedelta(days=1)}" 
        """
    )

    mysql_dic = {g: (t, c) for g, t, c in cursor.fetchall()}  # gid : title

    ### mysql 에 있는 것 중 api 에 없는것을 찾아야 함
    del_gid = []
    correct_dic = {}  # gid : 바꿀제목
    for gid in mysql_dic:
        # print(mysql_dic[gid][1], end=' ')
        if gid not in [*api_dic]:  ## mysql에 있는 gid가 api에는 없는경우  ==> 삭제
            #삭제할거
            if clean0:
                print('\n============')
                clean0 = False
            del_gid.append(gid)
            print(f"삭제 : {gid} / {mysql_dic[gid][0]}")

        elif api_dic[gid] != mysql_dic[gid][0]:  # gid가 있긴 한데 title이 다를 경우 ==> 수정
            if clean0:
                print('\n============')
                clean0 = False
            print(f"제목 수정 : {gid} / {mysql_dic[gid][0]} => {api_dic[gid]}  ")
            correct_dic[gid] = api_dic[gid]
        else:
            # print("이상없음")
            pass

    num_deleted = len(del_gid) # 삭제 수
    num_corrected = len(*[correct_dic]) # 수정 수
    ## 삭제  실행
    if len(del_gid) >0:
        cursor.execute(
            f"""
                delete from news_recommend.news_ago where gid in ({','.join(del_gid)})
                """
        )

    ## 수정 실행
    sql = """update news_recommend.news_ago set title=%s where gid=%s"""
    cursor.executemany(sql, [(value, key) for key, value in correct_dic.items()])
    db.commit()

    ## 활동 정리
    cursor.execute("""
    select count(*), max(createtime), min(createtime) from news_recommend.news_ago
    """)
    after_count, after_max, after_min = cursor.fetchone()

    return before_count, before_max, before_min, after_count, after_max, after_min, num_recieve, num_deal, num_doc2vec, num_deleted, num_corrected, clean0

if __name__ == '__main__':
    clean0 = True ## 줄바꾸기를 위한 장치.  clean0=True 일 경우 '\r'을 통해 '마지막 수신' 이 같은 자리에 계속 표시되게 함. clean0이 False로 바뀔 때 \n 을 통해 \r 을 지움.
    while True:
        now0 = datetime.now()
        before_count, before_max, before_min, after_count, after_max, after_min, num_recieve, num_deal, num_doc2vec, num_deleted, num_corrected, clean0 = updater(clean0)
        if num_doc2vec !=0 or num_deleted != 0 or num_corrected !=0: #처리한게 하나라도 있으면.
            if clean0:
                print('\n============')
                clean0 = False
            print(f"마지막 업데이트 : {now0} // mysql : {before_count} -> {after_count} // api {num_recieve}개 받아 {num_doc2vec}개 전환// {num_deleted}개 삭제 {num_corrected}개 수정")
            print("============")
        else:  # 처리한 게 하나도 없을 경우.
            clean0 =True
            print(f"\r마지막 수신 : {now0}",end='')
        time.sleep(30)
