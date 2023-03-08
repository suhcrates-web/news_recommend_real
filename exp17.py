import redis
from redis import Redis, ConnectionPool
import numpy as np

pool2 = ConnectionPool(host='localhost', port=6379, db=2)
r2 = redis.Redis(connection_pool=pool2)
print(np.random.rand(50))
print(np.random.rand(50).shape)
r2.set('temp', np.random.rand(50).astype('float32').tobytes())

temp = np.frombuffer(r2.get('temp'), dtype='float32')
print(temp.dtype)
print(np.frombuffer(r2.get('temp')).shape)

pool1 = ConnectionPool(host='localhost', port=6379, db=1)
r1 = redis.Redis(connection_pool=pool1)

test = np.frombuffer(r1.get('117853519'),dtype='float32')
print(test.dtype)
print(type(test))

r2.set('test',test.tobytes())
print(np.frombuffer(r2.get('test'),dtype='float32'))

test2 = test+temp
print(test2)
r2.set('test2', test2.tobytes())
print(np.frombuffer(r2.get('test2'),dtype='float32'))
