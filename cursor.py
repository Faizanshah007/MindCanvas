import win32gui
import time
import numpy as np
import math
f=open("SpeedNew.txt",'w')
f.truncate()
ts=time.time()
slots=0
try:
    while True:
        x,y=win32gui.GetCursorPos()
        f.write("{0},{1}\n".format(x,y))
        if(time.time()-ts>5):
            f.write("9999,9999\n")
            slots+=1
            ts=time.time()
except KeyboardInterrupt:
    print('\n')
f.close()
f1 = open('SpeedNew.txt','rt')
points = np.loadtxt(f1,delimiter=',')
xcord = points[:,0]
ycord = points[:,1]
i=0
dist=[]
speeds=[]
for j in range(slots):
    while(xcord[i+1]!=9999):
        xdiff=xcord[i+1]-xcord[i]
        ydiff=ycord[i+1]-ycord[i]
        dist.append(math.sqrt(pow(xdiff,2)+pow(ydiff,2)))
        i+=1
    speeds.append(sum(dist)/5)
    dist=[]
    i=i+2
print("No. of slots:",slots)
print("Default speed:",speeds[0])
for k in range(1,len(speeds)):
    print("Speed Difference",k,"=",(speeds[k]-speeds[0]))









