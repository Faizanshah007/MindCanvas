from sklearn import tree
import numpy as np
import math
import pandas as pd
import sklearn
f=open('apnadata1.txt','rt')
mydata=np.loadtxt(f,delimiter=',')
feat=mydata
xdiff=[0,0,0,0,0,0,0,0,0,0,0,0,0,0]
ydiff=[0,0,0,0,0,0,0,0,0,0,0,0,0,0]
dist=[0,0,0,0,0,0,0,0,0,0,0,0,0,0]
tdist=np.array([0,0])
tdist=tdist.reshape(-1,1)
for a in range(2):
    i=a*5
    for i in range(i,i+4):
        xdiff[i]=feat[i+1][0]-feat[i][0]
        ydiff[i]=feat[i+1][1]-feat[i][1]
        dist[i]=math.sqrt(pow(xdiff[i],2)+pow(ydiff[i],2))
        tdist[a]=tdist[a]+dist[i]
features=tdist
labels=["Calm","Panicked"]
clf=tree.DecisionTreeClassifier()
clf=clf.fit(features,labels)
i=10
tot_dist=0
for i in range(i,i+4):
        xdiff[i]=feat[i+1][0]-feat[i][0]
        ydiff[i]=feat[i+1][1]-feat[i][1]
        dist[i]=math.sqrt(pow(xdiff[i],2)+pow(ydiff[i],2))
        tot_dist=tot_dist+dist[i]
print(clf.predict([[tot_dist]]))



