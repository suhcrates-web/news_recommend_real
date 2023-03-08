
#####여러 경우의 수 고려

import numpy as np
import timeit
import json
import time
import redis
from redis import Redis, ConnectionPool
from collections import Counter
import mysql.connector

config = {
    'user' : 'root',
    'password': 'Seoseoseo7!',
    'host':'localhost',
    # 'database':'shit',
    'port':'3306'
}




test_ga = ['117995083', '117867403', '117996813', '117828556', '118058018', '117766432', '117845883', '117836563', '117776449', '117925227', '117846976', '118100453', '117848011', '117815088', '118100341', '117874258', '117853519', '118147936', '118081626', '117924726', '117779785', '118136183', '117897837', '117747817', '117752456', '117905513', '117851462', '117906542', '117871865', '117784810', '117982566', '117890586', '117845041', '117811088', '117829369', '118021422', '117821187', '117808078', '118024104', '117912900', '117930591', '117962224', '117819718', '117800029', '117815540', '118143903', '118138324', '117894057', '117939814', '117775665', '117764939', '118048995', '117852407', '117791161', '117808088', '118051427', '118000658', '118100501', '118111962', '118053485', '118138576', '117981492', '117986050', '117996057', '117999506', '117873114', '117818706', '118040009', '118021295', '117905543', '117798009', '117977012', '118084414', '118037504', '117819349', '118103786', '117993682', '118086577', '117799500', '117819353', '117962258', '118135957', '117891169', '117808228', '117989752', '117994192', '117854321', '117839518', '117808139', '117912390', '118030905', '117920947', '117774769', '117905690', '117985844', '118014919', '117887043', '118053338', '117867971', '117787409', '117979229', '118155301','1181553000','1181553000','1181553000','1181553000','1181553000','1181553000','1181553000','1181553000','1181553000','1181553000','1181553000','1181553000','1181553000','1181553000','1181553000','1181553000','1181553000','1181553000','1181553000','1181553000','1181553000','1181553000','1181553000','1181553000','1181553000','1181553000','1181553000','1181553000','1181553000','1181553000','1181553000','1181553000','1181553000','1181553000','1181553000','1181553000','1181553000','1181553000','1181553000','1181553000','1181553000','1181553000','1181553000','1181553000']

def find_10_alt(tot_mat, user_vector):
    points = np.matmul(tot_mat, user_vector)
    top10 = np.argsort(points)[::-1][:10]
    return top10


pool = ConnectionPool(host='localhost', port=6379, db=0)
pool1 = ConnectionPool(host='localhost', port=6379, db=1)
pool2 = ConnectionPool(host='localhost', port=6379, db=2)
r = redis.Redis(connection_pool=pool)
r1 = redis.Redis(connection_pool=pool1)
r2 = redis.Redis(connection_pool=pool2)


# r1 = redis.Redis(host='localhost', port=6379, db=1)
# r1.flushdb()
# import make_test_user_db
p = 0.3
time0 = []
time1 = []
result0 = []
result1 = []
for _ in range(2000):
    # time.sleep(3)
    gid = test_ga[np.random.randint(0, len(test_ga))]
    ga = gid
    start = timeit.default_timer()
    #######

    for _ in range(3):
        try:  # 그냥 아무이유없이 redis에서 None 이 나오는 경우가 매우 드물게 있어서
            if gid is None:   # 사용자에게서 gid 가 안옴
                u_vec = r1.get(ga)
                if u_vec == None:  # 사용자 ga에 해당하는 벡터가 없음
                    #완전히 새로운 추천
                    u_vec = r2.get('temp')
                    g_vec = u_vec
                else: #사용자 ga에 해당하는 벡터가 있음
                    g_vec = u_vec
            else: # 사용자에게서 gid 가 옴
                g_vec = r.get(gid)
                u_vec = r1.get(ga)

                if u_vec is not None: #ga에 해당하는 벡터가 있음
                    if g_vec is not None : #gid에 해당하는 벡터가 있음
                        pass #걍 하면 됨

                    else: #gid에 해당하는 벡터가 없음
                        g_vec = u_vec # 유저 벡터를 기사 벡터로 씀 (이전에 봤던게 더 강화됨)

                else: #ga에 해당하는 벡터가 없음. 처음오는 손님
                    if g_vec is not None: # gid에 해당하는 벡터는 있음
                        u_vec = g_vec
                    else: # gid에 해당하는 벡터도 없음
                        #완전히 새로운 추천
                        u_vec = r2.get('temp')
                        g_vec = u_vec

            u_vec = np.frombuffer(u_vec, dtype='float32')
            g_vec = np.frombuffer(g_vec, dtype='float32')
            u_vec = (1-p) * g_vec + p * u_vec
            r1.set(ga,u_vec.tobytes())
            mat = r2.get('mat')
            mat = np.frombuffer(mat).reshape(700, 50)
            top10 = list(find_10_alt(mat,u_vec))
            a = r2.get('title')
            title_list = json.loads(a)
            url_list = json.loads(r2.get('url'))
            thumburl_list = json.loads(r2.get('thumburl'))
            dics1 = {}
            for i, x in enumerate(top10):
                dics1[i] = {'title':title_list[x], 'url':url_list[x], 'thumburl':thumburl_list[x]}
            break
        except Exception as e:
            print(e)
    end = timeit.default_timer()
    # print(end-start)
    time1.append(end - start)


print("==============")
print(time1)
print(dics1)
# print("==============")
# print(max(time0))
# print(min(time0))
# print(np.mean(time0))
# print(sum(time0))
print("==============")
print(max(time1))
print(min(time1))
print(np.mean(time1))
print(sum(time1))

