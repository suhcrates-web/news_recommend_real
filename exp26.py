import redis
from redis import Redis, ConnectionPool
import numpy as np

pool5 = ConnectionPool(host='localhost', port=6379, db=5)
r5 = redis.Redis(connection_pool=pool5)


for i in range(3000000):
    r5.set(f"{i}1234",np.random.randint(1000000))