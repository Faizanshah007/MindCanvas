import ctypes
import win32gui
import time
import math
import atexit 


initial_mouse_speed = ctypes.c_int()


def dpi(x=10) :
    
    #   1 - slow
    #   10 - standard
    #   20 - fast

    global initial_mouse_speed

    get_mouse_speed = 112   # 0x0070 for SPI_SETMOUSESPEED
    ctypes.windll.user32.SystemParametersInfoA(get_mouse_speed, 0, ctypes.byref(initial_mouse_speed), 0)

    def setspeed(x):
        set_mouse_speed = 113   # 0x0071 for SPI_SETMOUSESPEED
        ctypes.windll.user32.SystemParametersInfoA(set_mouse_speed, 0, x, 0)

    setspeed(x)
    atexit.register(setspeed,initial_mouse_speed.value)

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


def average_speed():

    while condition=='on':
    

        ts = time.time()
    

        try:
            x, y = win32gui.GetCursorPos()
            #    time.sleep(0.05)
            c, d = win32gui.GetCursorPos()
            dis = dis + math.sqrt(((x - c) ** 2) + ((y - d) ** 2))

        except KeyboardInterrupt:
            time_diff = time.time() - ts
    time_diff = time.time() - ts
    print(dis / time_diff, " : Speed")
    return dis 

def onn():
    condition = 'on'
    dpi(10)

def off():
    condition="off"

atexit.register(off)



onn()
    
'''    
    






