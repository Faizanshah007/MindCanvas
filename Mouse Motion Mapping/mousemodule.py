from rprint import print
import win32gui
import atexit
import ctypes
import time
import math


initial_mouse_speed = int()


# Set mouse speed

def dpi(x=10) :
    global initial_mouse_speed

    #   1 - slow
    #   10 - standard
    #   20 - fast

    def getspeed():
        x = ctypes.c_int()
        get_mouse_speed = 112   # 0x0070 for SPI_GETMOUSESPEED
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


def player_average_speed():
    global condition
    dist = 0
    start = time.time()
    x0, y0 = win32gui.GetCursorPos()

    while condition == 'on':
        x1, y1  = win32gui.GetCursorPos()
        dist    = dist + (((x1 - x0)** 2) + ((y1 - y0)** 2)) ** (1/2)
        x0, y0  = x1, y1

    end        = time.time()
    time_diff  = end - start
    speed      = dist / time_diff
    print("Average speed is ", speed)
    return speed


def on():
    global condition
    condition = "on"
    player_average_speed()


def off():
    global condition
    condition = "off"
