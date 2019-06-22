# "#~" - Variable's value not to be changed

import sys, os, time, pygame
from pygame.locals import *

if "anagram_generator" not in sys.modules :
    from anagram_generator import *

# Expresssion

cur_exp = None
exp_list = list()
temp_exp_list = list()

def net_exp():
    global temp_exp_list
    temp_dict = dict()
    for exp_data in temp_exp_list:
        if(exp_data[0] in temp_dict):
            temp_dict[exp_data[0]] += exp_data[1]
        else:
            temp_dict[exp_data[0]] = exp_data[1]
    try: ##
        print(sorted(temp_dict.items(), reverse = True, key = lambda tup : tup[1])[0][0])
    except:
        pass
    temp_exp_list.clear()


# Monitoring Clicks

click_count = 0
right_clicks = 0
wrong_clicks = 0


# Subprocess List

subproc_list = list()


# Game Status

stat = 'None'


# Timer

timer = 0


# List of Linked words

lnkdlist = pygame.sprite.Group()

# List of buttons

buttonlist = pygame.sprite.Group()



# Initializing Pygame

pygame.init()


#~Path

root_dir = os.path.join(os.path.dirname(sys.argv[0]), 'Media')
sys.path.insert(0, os.path.abspath('.\\..\\Mouse Motion Mapping'))
sys.path.insert(0, os.path.abspath('.\\..\\Expression Recognition'))

#~Anagram Data

anagpool   = Pre_setup.get()
anagselec  = produce()


#~Window Dimension

window_width = 1000 #max - 1366
window_height = int(window_width*0.5)#max - 768


#~Fonts

font_dir = os.path.join(os.path.dirname(sys.argv[0]), 'Fonts')
txtfont1 = pygame.font.Font(os.path.join(font_dir, "Courier New", "COURBI.TTF"), int((1/13)*window_height))
txtfont2 = pygame.font.Font(os.path.join(font_dir, "Copperplate Gothic", "COPRGTB.TTF"), int((1/25)*window_height))


#~Colors

white   = (255,255,255)
cyan    = (0, 255, 255)
blue    = (0,0,255)
black   = (0,0,0)
orange  = (255, 165, 0)
green   = (0,255,0)
red     = (255,0,0)
yellow  = (255,255,0)
purple  = (160,32,240)

bgcolor = black


# Wait function

def waitforkey():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type ==  pygame.MOUSEBUTTONUP:
                return
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return


# End Subrocesses

import signal

def release_proc():
    for proc in subproc_list:
        os.kill(proc.pid, signal.CTRL_C_EVENT)


# Terminate

def terminate():
    pygame.quit()
    release_proc()
    sys.exit()


# Render Text

def drawtext(text,font,surface,x,y,colour = black):
    textobj = font.render(text,1,colour)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj, textrect)


# Answers

ignorelist = list() #Stores words which have 0 possible anaglink

def ansGen():
    ans = list()
    sub = list()
    a = list()
    for tp in anagpool:
        sub.clear()
        for wrd in anagselec:
            if(wrd in tp):
                sub.append(wrd)
        a = sub[:]

        if(len(a)==1):
            ignorelist.append(a)

        if(len(a)>1):
            ans.append(a)

    return(ans)

ans = ansGen() #Contains all the anaglinks
ans_copy = ans[:] #~


# Result

Score = 0
TimeBonus = 0


# Bringing window to foreground

#CODE IMPORTED FROM:
#https://www.blog.pythonlibrary.org/2014/10/20/pywin32-how-to-bring-a-window-to-front/'''

import win32gui, win32com.client

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
