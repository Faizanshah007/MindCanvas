import sys, os

## import atexit
## atexit.register(print,"Exiting Core")

# Path
MEDIA_DIR = os.path.join(os.path.dirname(sys.argv[0]), 'Media')
sys.path.insert(0, os.path.abspath('.\\..\\Mouse Motion Mapping'))


from rprint import print
import anagram_generator
import mousemodule


import threading
import pygame
import pickle
import time

# For Window Manipulations
import win32api, win32gui, win32com.client, win32process

# For manipulating window's master volume
import pycaw.pycaw
import ctypes
import comtypes


# Facial Expresssion Data & Function

cur_expr = None
expr_list = list()       # Contains all the captured facial expression throught the game
task_expr_list = list()  # Contains all the captured facial expression during the task
selected_exprs = list()  # Stores the net expression given by net_expr()

def net_expr():
    temp_dict = dict()

    # Finding the expression with maximum weightage
    for expr_data in task_expr_list:
        if(expr_data[0] in temp_dict):
            temp_dict[expr_data[0]] += expr_data[1]
        else:
            temp_dict[expr_data[0]] = expr_data[1]
    try:
        selected_exprs.append(sorted(temp_dict.items(), reverse = True, key = lambda tup : tup[1])[0][0])
    except:
        selected_exprs.append("X")
    task_expr_list.clear()


# Game Status
stat = 'None'


# Timer
TOTAL_TIME = 60  # Game Duration
timer = 0


# Mousemodule Data
players_initial_avg_speed_capture_time = TOTAL_TIME / 4
players_initial_avg_speed = None

def set_dpi(x):
    return mousemodule.dpi(x)

# Monitoring Clicks
click_count  = 0
button_clicks = 0
wrong_clicks = 0


# Preparing pygame sound mixer before initialization
pygame.mixer.pre_init(22050, -16, 2, 64)

# Initializing Pygame
pygame.init()


# List of Linked words
lnkdlist = pygame.sprite.Group()

# List of buttons
buttonlist = pygame.sprite.Group()


# Anagram Data
ANAGPOOL     = anagram_generator.Pre_setup.get()
ANAGSCHOSEN  = anagram_generator.produce()


# Window Dimension
WINDOW_WIDTH  = int(win32api.GetSystemMetrics(0) * (125 / 192))  # Needs to be greater than or equal to 500
WINDOW_HEIGHT = int(WINDOW_WIDTH * 0.5)


# Fonts
FONT_DIR = os.path.join(os.path.dirname(sys.argv[0]), 'Fonts')
TXT_FONT_1 = pygame.font.Font(os.path.join(FONT_DIR, "Courier New", "COURBI.TTF"), int((1/13)*WINDOW_HEIGHT))
TXT_FONT_2 = pygame.font.Font(os.path.join(FONT_DIR, "Copperplate Gothic", "COPRGTB.TTF"), int((1/25)*WINDOW_HEIGHT))


# Colors
colors = {
'WHITE'               : (255, 255, 255),
'BLUE_VARIANT_1'      : (0, 110, 255),
'BLUE'                : (0, 0, 255),
'BLACK'               : (0, 0, 0),
'ORANGE'              : (255, 165, 0),
'GREEN'               : (0, 255, 0),
'RED'                 : (255, 0, 0),
'YELLOW'              : (255, 255, 0),
'PURPLE'              : (160, 32, 240)
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
initial_volume = volume.GetMasterVolumeLevel()  # Store initial volume
mute_stat = dict()  # Stores initial mute status of other applications & Master volume
mute_stat["Master"] = volume.GetMute()

# Handles mute/unmute options
def focus_game_sound(pid):

    sessions = pycaw.pycaw.AudioUtilities.GetAllSessions()

    if(pid != -1):

        volume.SetMute(0,None)  # Ensure Master volume remains unmuted during the game

        for session in sessions:
            current_app_pid = session.ProcessId
            if(current_app_pid != pid):

                if(current_app_pid not in mute_stat.keys()):
                    mute_stat[current_app_pid] = session.SimpleAudioVolume.GetMute()

                session.SimpleAudioVolume.SetMute(1, None)  # Mute if its not the game

            else:
                session.SimpleAudioVolume.SetMute(0, None)  # Ensure unmute state if its the game

    else:  # Set other applications to their original mute/unmute status

        volume.SetMute(mute_stat["Master"],None)

        for session in sessions:
            current_app_pid = session.ProcessId
            if(current_app_pid in mute_stat):
                session.SimpleAudioVolume.SetMute(mute_stat[current_app_pid], None)


# Regulates volume level during the game
def check_volume():

    focus_game_sound(os.getpid())

    if(volume.GetMasterVolumeLevel() < -11.8):
        volume.SetMasterVolumeLevel(-11.8, None)  # Maintain volume at 45% or above




# Terminate

def terminate():
    pygame.quit()

    # Restore volume properties
    volume.SetMasterVolumeLevel(initial_volume, None)
    focus_game_sound(-1)

    switch_file = open(os.path.abspath('.\\..\\switch'),"wb")
    pickle.dump("off",switch_file)
    switch_file.close()
    result_file = open("Result.txt","a")
    result_file.write("\n")  # Indicating the end of a particular game's result inside the file
    result_file.close()
    mousemodule.off()  # Release mousemodule
    set_dpi(-1)  # Reset DPI
    sys.exit()


# Render Text

def drawtext(text,font,surface,x,y,colour = colors['BLACK']):
    textobj          = font.render(text,1,colour)
    textrect         = textobj.get_rect()
    textrect.center  = (x, y)
    surface.blit(textobj, textrect)


# Answer Generation Data & Function

ignorelist   = list()  # Stores words which have 0 possible anaglink

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
# https://www.programcreek.com/python/example/100815/win32process.GetWindowThreadProcessId

def foregroundWindow(pid):

    try:
        print("here")
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')

        def get_hwnds(pid):
            """return a list of window handlers based on it process id"""
            def callback(hwnd, hwnds):
                if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
                    _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                    if found_pid == pid:
                        hwnds.append(hwnd)
                return True
            hwnds = []
            win32gui.EnumWindows(callback, hwnds)
            return hwnds
            
        win32gui.ShowWindow(get_hwnds(pid)[0],5)
        win32gui.SetForegroundWindow(get_hwnds(pid)[0])
        return True

    except:
        return False
