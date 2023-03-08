### ga 번호가 호출로 왔다고 했을 때  유저 벡터, 기사 벡터 각각 꺼내기

import redis
import json
import numpy as np
import timeit
r = redis.Redis(host='localhost', port=6379, db=0)
r1 = redis.Redis(host='localhost', port=6379, db=1)

## r1 유저가  ga와 gid 를 보냄 (여기선 걍 ga = gid) 임.
# r1에서 ga에 해당하는 vec을 꺼냄.
# r0 에서 gid에 해당하는 vec을 꺼냄
# 둘을 섞음


test_ga = [117613119,117634894,117636851,117636957,117637748,117637908,117637911,117637913,117637915,117637916,117637917,117637922,117637923,117637924,117638121,117638182,117638235,117638241,117638243,117638357,117638362,117638539,117638807,117639038,117639044,117639048,117639051,117639068,117639071,117639074,117639090,117639280]

time0 = []
for _ in range(2000):
    gid = test_ga[np.random.randint(0, len(test_ga))]
    start = timeit.default_timer()
    ga = gid
    g_vec = np.array(json.loads(r.get(gid)))
    u_vec = np.array(json.loads(r1.get(gid)))
    end = timeit.default_timer()
    time0.append(end-start)

print(max(time0))
print(min(time0))
print(np.mean(time0))