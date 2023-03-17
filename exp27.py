##### 대용량 redis 반응속도 실험 ####

import redis
from redis import Redis, ConnectionPool
import numpy as np
import timeit
import time

pool5 = ConnectionPool(host='localhost', port=6379, db=5)
r5 = redis.Redis(connection_pool=pool5)

pool = ConnectionPool(host='localhost', port=6379, db=0)
r = redis.Redis(connection_pool=pool)


# ####### 대용량 반응속도 실험 ######
# start = timeit.default_timer()
# r.get('118358335')
# # r.set('1183583352',2)
# end = timeit.default_timer()
# print(end-start)
#
# start = timeit.default_timer()
# r5.get('11234')
# # r5.set('10000', 1)
# end = timeit.default_timer()
# print(end-start)
#
# start = timeit.default_timer()
# r.get('118358335')
# # r.set('1183583352',2)
# end = timeit.default_timer()
# print(end-start)


#####  interval 에 따른 반응속도 실험 #####
 ## 인터벌이 아무리 길어도 속도는 같은디
for _ in range(100):
    start = timeit.default_timer()

    r.get('118358335')
    end = timeit.default_timer()
    a=end-start
    print(end-start)
    time.sleep(1)