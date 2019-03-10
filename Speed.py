import pyautogui as pag
import pynput
from pynput.mouse import Listener
import threading
import logging
import math
import numpy as np
f=open("Speed.txt","w")
f.truncate()
f.close()
logging.basicConfig(filename=("Speed.txt"), level=logging.DEBUG, format='%(message)s')
try:
	while True:
		x,y=pag.position()
		e=threading.Event()
		e.wait(0.05)
		logging.info("{0},{1}".format(x,y))
except KeyboardInterrupt:
	print('\n')
f1 = open('Speed.txt','rt')
mydata1 = np.loadtxt(f1,delimiter=',')
total_distance = 0
xdiff = [0]*int(len(mydata1))
ydiff = [0]*int(len(mydata1))
dist = [0]*int(len(mydata1))
speed=[]
for b in range(100):
        xdiff[b] = mydata1[b+1][0]-mydata1[b][0]
        ydiff[b] = mydata1[b+1][1]-mydata1[b][1]
        dist[b] = math.sqrt(pow(xdiff[b],2)+pow(ydiff[b],2))
        total_distance = total_distance+dist[b]
default_speed = total_distance/5
print("Default speed =",default_speed)
cal_len = int(len(mydata1)/100)
for c in range(1,cal_len):
    sample_distance=0
    d = c*100
    for d in range(d,d+100):
        xdiff[d] = mydata1[d+1][0]-mydata1[d][0]
        ydiff[d] = mydata1[d+1][1]-mydata1[d][1]
        dist[d] = math.sqrt(pow(xdiff[d],2)+pow(ydiff[d],2))
        sample_distance = sample_distance+dist[d]
    speed.append(sample_distance/5)
for i in range(len(speed)):
    speed[i]=speed[i]-default_speed
    print("Speed_Differnece",i+1,"=",speed[i])