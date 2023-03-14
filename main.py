from fastapi import FastAPI
import numpy as np
import timeit
import json
import redis
from redis import Redis, ConnectionPool
import uvicorn
from pydantic import BaseModel
from database import config


def find_10_alt(tot_mat, user_vector):
    points = np.matmul(tot_mat, user_vector)
    top10 = np.argsort(points)[::-1][:10]
    return top10
#
# class item0(BaseModel):
#     ga: str
#     gid: str =None
#     num0: int =10


app = FastAPI()



pool = ConnectionPool(host='localhost', port=6379, db=0)
pool1 = ConnectionPool(host='localhost', port=6379, db=1)
pool2 = ConnectionPool(host='localhost', port=6379, db=2)
r = redis.Redis(connection_pool=pool)
r1 = redis.Redis(connection_pool=pool1)
r2 = redis.Redis(connection_pool=pool2)

@app.get("/{ga}/{gid}")
async def hello(ga:str, gid:str=None):
    gid = None if '_' else gid
    p = 0.3
    time0 = []
    time1 = []
    result0 = []
    result1 = []
    # time.sleep(3)
    start = timeit.default_timer()
    #######
    dics1= {}
    for _ in range(3):
        try:  # 그냥 아무이유없이 redis에서 None 이 나오는 경우가 매우 드물게 있어서
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
            u_vec = (1 - p) * g_vec + p * u_vec
            r1.set(ga, u_vec.tobytes())
            mat = r2.get('mat')
            mat = np.frombuffer(mat).reshape(700, 50)
            top10 = list(find_10_alt(mat, u_vec))
            a = r2.get('title')
            title_list = json.loads(a)
            url_list = json.loads(r2.get('url'))
            thumburl_list = json.loads(r2.get('thumburl'))
            dics1 = {}
            for i, x in enumerate(top10):
                dics1[i] = {'title': title_list[x], 'url': url_list[x], 'thumburl': thumburl_list[x]}
            break
        except Exception as e:
            print(e)
    end = timeit.default_timer()
    # print(end-start)
    time1.append(end - start)

    return dics1

if __name__ == '__main__':
    uvicorn.run(app, port=8001, host='0.0.0.0')
    # uvicorn.run(app, port=8001, host='localhost')

    #####