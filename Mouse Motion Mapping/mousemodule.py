import ctypes
import win32gui
import time
import math
import atexit 


initial_mouse_speed = int()


def dpi(x=10) :

    global initial_mouse_speed
    
    #   1 - slow
    #   10 - standard
    #   20 - fast

    def getspeed():
        x = ctypes.c_int()
        get_mouse_speed = 112   # 0x0070 for SPI_SETMOUSESPEED
        ctypes.windll.user32.SystemParametersInfoA(get_mouse_speed, 0, ctypes.byref(x), 0)
        return x.value

    def setspeed(x):
        temp_speed = getspeed()
        x = ctypes.c_int(x)
        if(temp_speed != x.value):
            set_mouse_speed = 113   # 0x0071 for SPI_SETMOUSESPEED
            ctypes.windll.user32.SystemParametersInfoA(set_mouse_speed, 0, x, 0)

    initial_mouse_speed = getspeed()
    setspeed(x)
    atexit.register(setspeed,initial_mouse_speed)

    return setspeed

'''
expression='neutral'
default_dis = 0
dis = 0
condition = ''   
    
def default():
    
    while expression == 'neutral':


        ts = time.time()
    

        try:

            
            x, y = win32gui.GetCursorPos()
        # time.sleep(0.05)
            c, d = win32gui.GetCursorPos()
            default_dis = dis + math.sqrt(((x - c) ** 2) + ((y - d) ** 2))

        except KeyboardInterrupt:
            time_diff = time.time() - ts
            speed = default_dis  / time_diff

    time_diff = time.time() - ts
    speed = default_dis  / time_diff        
    print(speed, " : Speed")

    
    return speed 

'''
def average_speed():
    dis = 0
    global condition
    start = time.time()
    
    while condition=='on':
        
        x, y = win32gui.GetCursorPos()
        #    time.sleep(0.05)
        c, d = win32gui.GetCursorPos()
        dis = dis + math.sqrt(((x - c) ** 2) + ((y - d) ** 2))
            

    end = time.time()
    time_diff=end-start
    speed=dis/time_diff
    print("average speed is " ,speed)
    return speed    

def onn():
    global condition
    condition="on"
    average_speed()
    
  

def off():
    global condition
    condition="off"
 
    






