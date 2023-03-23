# main_v2
from fastapi import FastAPI
import numpy as np
import json
import redis
from redis import ConnectionPool
import uvicorn
from datetime import datetime
import traceback

def find_10_alt(tot_mat, user_vector, gisa_vector):
    sorted_g = np.argsort(np.matmul(tot_mat, gisa_vector))[::-1][:14]
    sorted_u_origin = np.argsort(np.matmul(tot_mat, user_vector))[::-1]
    sorted_u = sorted_u_origin[:37][~np.isin(sorted_u_origin[:37], sorted_g)]
    indices = np.random.choice(14, size=5, replace=False)
    indices.sort()
    zero = sorted_g[indices]
    first = sorted_u[indices]
    second = sorted_u_origin[-3:]
    top10 = np.concatenate((zero, first, second))
    return top10

app = FastAPI()

pool = ConnectionPool(host='localhost', port=6379, db=0)
pool1 = ConnectionPool(host='localhost', port=6379, db=1)
pool2 = ConnectionPool(host='localhost', port=6379, db=2)
pool3 = ConnectionPool(host='localhost', port=6379, db=3)
r = redis.Redis(connection_pool=pool)
r1 = redis.Redis(connection_pool=pool1)
r2 = redis.Redis(connection_pool=pool2)
r3 = redis.Redis(connection_pool=pool3)

@app.get("/{ga}/{gid}")
async def hello(ga:str, gid:str=None):
    gid = None if gid=='_' else gid
    r3.rpush(datetime.now().strftime('%Y%m%d%H:%M')[:-1],f'["{ga}","{gid}"]')
    p = 0.35
    dics1= {}
    for _ in range(3):
        try:  # # redis에서 이유 없이 None 이 나오는 경우가 매우 드물게 있어서 3번 시도.
            if gid is None:  # 사용자에게서 gid 가 안옴
                u_vec = r1.get(ga)
                if u_vec == None:  # 사용자 ga에 해당하는 벡터가 없음
                    # 완전히 새로운 추천
                    u_vec = r2.get('temp')
                    g_vec = u_vec
                else:  # 사용자 ga에 해당하는 벡터가 있음
                    g_vec = u_vec
            else:  # 사용자에게서 gid 가 옴
                g_vec = r.get(gid)
                u_vec = r1.get(ga)
                if u_vec is not None:  # ga에 해당하는 벡터가 있음
                    if g_vec is not None:  # gid에 해당하는 벡터가 있음
                        pass  # 걍 하면 됨
                    else:  # gid에 해당하는 벡터가 없음
                        g_vec = u_vec  # 유저 벡터를 기사 벡터로 씀 (이전에 봤던게 더 강화됨)
                else:  # ga에 해당하는 벡터가 없음. 처음오는 손님
                    if g_vec is not None:  # gid에 해당하는 벡터는 있음
                        u_vec = g_vec
                    else:  # gid에 해당하는 벡터도 없음
                        # 완전히 새로운 추천
                        u_vec = r2.get('temp')
                        g_vec = u_vec
            u_vec = np.frombuffer(u_vec, dtype='float32')
            g_vec = np.frombuffer(g_vec, dtype='float32')

            mat = r2.get('mat')
            mat = np.frombuffer(mat, dtype='float32').reshape(-1, 50)
            top10 = list(find_10_alt(mat, u_vec, g_vec))
            u_vec = (1 - p) * g_vec + p * u_vec
            r1.set(ga, u_vec.tobytes())
            r1.expire(ga, 2592000)  # 60*60*24*30 : 30일 뒤
            a = r2.get('title')
            title_list = json.loads(a)
            url_list = json.loads(r2.get('url'))
            thumburl_list = json.loads(r2.get('thumburl'))
            gid_list = json.loads(r2.get('gid2'))
            dics1 = {}
            for i, x in enumerate(top10):
                if gid != gid_list[x]:
                    dics1[i] = {'title': title_list[x], 'url': url_list[x], 'thumburl': thumburl_list[x]}
            break
        except Exception as e:
            traceback.print_exc()
            print(e)
    return dics1

# if __name__ == '__main__':
#     uvicorn.run(app, port=8001, host='localhost')
