from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
import redis
import numpy as np
from matplotlib import pyplot as plt



r1 = redis.Redis(host='localhost', port=6379, db=0)

keys0 = r1.keys('*')
mat = []

for i, key in enumerate(keys0):
    vec = r1.get(key)
    mat.append( np.fromstring(vec, dtype='float32'))
mat = np.array(mat)
scaler = MinMaxScaler(feature_range=(0, 1))
mat = scaler.fit_transform(mat)


### K-means 적용
before_sse = 1000000000000000
before_km = ''
for k in range(1,10):  # k에 1~10 숫자를 넣어봄
    km = KMeans(n_clusters = k)
    km.fit(mat)
    now_sse = km.inertia_
    if now_sse/before_sse > 0.5:
        print(k-1)
        break

    before_sse = now_sse
    before_km = km


km = before_km

print(km.cluster_centers_)
print(km.labels_)
print(np.bincount(km.labels_))

y_predicted = km.labels_

k= len(np.bincount(km.labels_))

pca = PCA(n_components=2)
pca.fit(mat)
mat_pca = pca.transform(mat)

dic = {}
for i in range(k):
    dic[f'df{i}'] = {'x': [], 'y': [], 'z':[]}
for n, i in enumerate(y_predicted):
    dic[f'df{i}']['x'].append(mat_pca[n,0])
    dic[f'df{i}']['y'].append(mat_pca[n,1])
    # dic[f'df{i}']['z'].append(mat[n,2])
for i in range(k):
    plt.scatter(dic[f'df{i}']['x'], dic[f'df{i}']['y'], label=i)
# plt.scatter(km.cluster_centers_[:,0],km.cluster_centers_[:,1],color='purple', marker='*', label='centroid')
plt.legend()
plt.show()