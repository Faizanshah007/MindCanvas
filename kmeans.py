import matplotlib.pyplot as plt
import seaborn as sns; sns.set()  # for plot styling
import numpy as np
X=np.loadtxt("kmeans.txt",delimiter=',')
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=5)
kmeans.fit(X)
labels = kmeans.predict(X)
#print(labels)
centers=kmeans.cluster_centers_
#print(centers)
Y=np.loadtxt("kmeans.txt",delimiter=',')
i=kmeans.predict(Y)
plt.scatter(X[:,0],X[:,1], c=labels, cmap='rainbow')  
plt.show()
