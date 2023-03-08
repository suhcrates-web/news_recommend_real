import redis
import numpy as np
import timeit
import json

####  from tostring   vs   json.loads

r3 = redis.Redis(host='localhost', port=6379, db=3)
vec0 = np.random.rand(1000)
r3.flushdb()
time0 = []
for _ in range(10000):
    start = timeit.default_timer()
    r3.set(_, vec0.tostring())
    np.fromstring(r3.get(_))
    end = timeit.default_timer()
    time0.append(end-start)
print(max(time0))
print(min(time0))
print(np.mean(time0))
# 0.008108099980745465
# 0.00010659999679774046
# 0.00013788982009573373
print("===============")

r3.flushdb()
time0 = []
vec0 = list(vec0)
for _ in range(10000):
    start = timeit.default_timer()
    r3.set(_, str(vec0))
    np.array(json.loads(r3.get(_)))
    end = timeit.default_timer()
    time0.append(end - start)
print(max(time0))
print(min(time0))
print(np.mean(time0))
# 0.0009387999889440835
# 0.000152900000102818
# 0.00018072138002316933


#### tostring : 평균시간은 더 짧은데 max 값은 10배 큼
#### 행렬이 길어질수록 tostring 이 훨 효율적임.
## tostring 쓰기로.