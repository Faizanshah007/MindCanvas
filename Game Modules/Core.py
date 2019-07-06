from rprint import print
import anagram_generator

import sys, os
import pygame
import pickle
import time

# For Window Manipulations
import win32api, win32gui, win32com.client

# For manipulating window's master volume
import pycaw.pycaw
import ctypes
import comtypes


# Facial Expresssion Data & Function  ##INSPECTING

cur_expr = None
expr_list = list()
temp_expr_list = list()

def net_expr():
    global temp_expr_list
    temp_dict = dict()
    for expr_data in temp_expr_list:
        if(expr_data[0] in temp_dict):
            temp_dict[expr_data[0]] += expr_data[1]
        else:
            temp_dict[expr_data[0]] = expr_data[1]
    try:  ##
        print(sorted(temp_dict.items(), reverse = True, key = lambda tup : tup[1])[0][0])
    except:
        pass
    temp_expr_list.clear()


# Monitoring Clicks
click_count  = 0
right_clicks = 0
wrong_clicks = 0


# Game Status  ##INSPECTING
stat = 'None'


# Timer  ##INSPECTING
timer = 0


# Initializing Pygame
pygame.init()


# List of Linked words  ##INSPECTING
lnkdlist = pygame.sprite.Group()

# List of buttons  ##INSPECTING
buttonlist = pygame.sprite.Group()


# Path  ##INSPECTING
ROOT_DIR = os.path.join(os.path.dirname(sys.argv[0]), 'Media')
sys.path.insert(0, os.path.abspath('.\\..\\Mouse Motion Mapping'))
sys.path.insert(0, os.path.abspath('.\\..\\Expression Recognition'))

# Anagram Data
ANAGPOOL     = anagram_generator.Pre_setup.get()
ANAGSCHOSEN  = anagram_generator.produce()


# Window Dimension
WINDOW_WIDTH  = int(win32api.GetSystemMetrics(0) * (125 / 192)) ##1000  # Needs to be greater than or equal to 500
WINDOW_HEIGHT = int(WINDOW_WIDTH * 0.5)


# Fonts
FONT_DIR = os.path.join(os.path.dirname(sys.argv[0]), 'Fonts')
TXT_FONT_1 = pygame.font.Font(os.path.join(FONT_DIR, "Courier New", "COURBI.TTF"), int((1/13)*WINDOW_HEIGHT))
TXT_FONT_2 = pygame.font.Font(os.path.join(FONT_DIR, "Copperplate Gothic", "COPRGTB.TTF"), int((1/25)*WINDOW_HEIGHT))


# Colors
colors = {
'WHITE'     : (255, 255, 255),
'CYAN'      : (0, 255, 255),
'BLUE'      : (0, 0, 255),
'SKY_BLUE'  : (135, 206, 235),
'BLACK'     : (0, 0, 0),
'ORANGE'    : (255, 165, 0),
'GREEN'     : (0, 255, 0),
'RED'       : (255, 0, 0),
'YELLOW'    : (255, 255, 0),
'PURPLE'    : (160, 32, 240)
}

bgcolor = colors['BLACK']  # Background color of the canvas


# Wait function

def waitforkey():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type ==  pygame.MOUSEBUTTONUP:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                return


# Ensure volume is atleast 72%
# https://github.com/AndreMiras/pycaw

devices = pycaw.pycaw.AudioUtilities.GetSpeakers()
interface = devices.Activate(pycaw.pycaw.IAudioEndpointVolume._iid_, comtypes.CLSCTX_ALL, None)
volume = ctypes.cast(interface, ctypes.POINTER(pycaw.pycaw.IAudioEndpointVolume))

def chkvolume():
    volume.SetMute(0,None)

    if(volume.GetMasterVolumeLevel() < -5):
        volume.SetMasterVolumeLevel(-5.0, None)  # Set volume at 72%

initial_volume = volume.GetMasterVolumeLevel()  # Store initial volume


# Terminate

def terminate():
    pygame.quit()
    volume.SetMasterVolumeLevel(initial_volume, None)
    out = open(os.path.abspath('.\\..\\switch'),"wb")
    pickle.dump("off",out)
    sys.exit()


# Render Text

def drawtext(text,font,surface,x,y,colour = colors['BLACK']):
    textobj          = font.render(text,1,colour)
    textrect         = textobj.get_rect()
    textrect.center  = (x, y)
    surface.blit(textobj, textrect)


# Answer Generation Data & Function

ignorelist   = list()  #Stores words which have 0 possible anaglink  ##INSPECTING

def ansGen():
    ans      = list()
    wrdTemp  = list()
    linkTemp = list()
    for tup in ANAGPOOL:
        wrdTemp.clear()
        for wrd in ANAGSCHOSEN:
            if(wrd in tup):
                wrdTemp.append(wrd)
        linkTemp = wrdTemp[:]

        if(len(linkTemp)==1):
            ignorelist.append(linkTemp)

        if(len(linkTemp)>1):
            ans.append(linkTemp)

    return(ans)

ans       = ansGen()  #Contains all the anaglinks
ANS_COPY  = ans[:]


# Result
Score     = 0
TimeBonus = 0


# Bringing window to foreground

# CODE IMPORTED FROM:
# https://www.blog.pythonlibrary.org/2014/10/20/pywin32-how-to-bring-a-window-to-front/

def foregroundWindow(name):
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')

    def windowEnumerationHandler(hwnd, top_windows):
        top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

    top_windows = []
    win32gui.EnumWindows(windowEnumerationHandler, top_windows)
    for i in top_windows:
        if name.lower() in i[1].lower():
            win32gui.ShowWindow(i[0],5)
            win32gui.SetForegroundWindow(i[0])
            break
