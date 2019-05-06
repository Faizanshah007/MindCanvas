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
Y=np.loadtxt("testpro.txt",delimiter=',')
i=kmeans.predict(Y)
# Ye niche ka part aise hi kuch bhi hai, uss din external sir ko dikhane ke liye
'''
f=open("op.txt","r+")
f.truncate()

if(i[1]==0):
	print("15%")
	f.write("15")
if(i[1]==1):
	print("35%")
	f.write("35")

if(i[1]==2):
	print("50%")
	f.write("50")

if(i[1]==3):
	print("75%")
	f.write("75")

if(i[1]==4):
	print("90%")
	f.write("90")
f.close()
'''



plt.scatter(X[:,0],X[:,1], c=labels, cmap='rainbow')  
plt.show()