import threading
import subprocess
import loading, Data
from Data import *


# Starting Expression Recognition Module

Data.subproc_list.append(subprocess.Popen("python label.py", shell=True, cwd = "D:\\faiza\\Documents\\GitHub\\Mind Canvas\\Expression Recognition"))


# Loading Game

from button import *
from Scoring_Algo import *
import freq_alpha
import time
import os, sys
import pickle
import mousemodule
from shutil import copyfile
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


# Set Mouse DPI

dpi_speed = 8 ##
check_speed = mousemodule.dpi(dpi_speed)


# Close loading window

time.sleep(5)
loading.root.destroy()


# Initializing window

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % loading.get_coord(window_width, window_height)

pygame.init()
pygame.display.set_caption("Anaglink")
Canvas = pygame.display.set_mode((window_width, window_height), pygame.NOFRAME)
pygame.event.set_grab(True)

Data.foregroundWindow("Anaglink")

subsurface = Canvas.subsurface((0, 0, window_width, (1 / 5) * window_height))


# Ensure volume is atleast 72%
# https://github.com/AndreMiras/pycaw

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

def chkvolume():

    volume.SetMute(0,None)
    
    if(volume.GetMasterVolumeLevel() < -5):
        volume.SetMasterVolumeLevel(-5.0, None) #72%


# Setting sprites

pygame.mixer.music.load(os.path.join(root_dir, "main.wav"))

loosemusic = pygame.mixer.Sound(os.path.join(root_dir, "game_over.wav"))
winmusic = pygame.mixer.Sound(os.path.join(root_dir, "winner.wav"))
linkedmusic = pygame.mixer.Sound(os.path.join(root_dir, "anaglinked.wav"))
incorrectmusic = pygame.mixer.Sound(os.path.join(root_dir, "incorrect.wav"))
fewsecsound = pygame.mixer.Sound(os.path.join(root_dir, "fewsecleft.wav"))

startimage = pygame.image.load(os.path.join(root_dir, "start.jpg"))
startimage = pygame.transform.scale( startimage, ( window_width, window_height ) )
startimagerect = startimage.get_rect()
startimagerect.centerx = window_width / 2
startimagerect.centery = window_height / 2

lostimage = pygame.image.load(os.path.join(root_dir, "lost.jpg"))
lostimage = pygame.transform.scale( lostimage, ( window_width, window_height ) )
lostimagerect = startimage.get_rect()
lostimagerect.centerx = window_width / 2
lostimagerect.centery = window_height / 2

wonimage = pygame.image.load(os.path.join(root_dir, "won.jpg"))
wonimage = pygame.transform.scale( wonimage, ( window_width, window_height ) )
wonimagerect = startimage.get_rect()
wonimagerect.centerx = window_width / 2
wonimagerect.centery = window_height / 2


# Button Plotting

def plotter(lst):

    for i in range(5):
        for j in range(5):
            Data.buttonlist.add( Button( Canvas, int(window_width * (1 / 20 + j / 5)), int(window_height * (1 / 4 + i * 1 / 7)), lst[j + 5 * i]) )


# Timer

totalTime = 60
timerRatio = (0.9) / totalTime

def update_timer():

    global clock

    Data.timer = time.time() - clock

    pygame.draw.rect(subsurface, cyan, (int(window_width * (1 / 20)), int(window_height * (15 / 100)), int(window_width * (0.9)), int(window_width * (1 / 50))), 2)

    return(pygame.draw.rect(subsurface, red, (int(window_width * (1 / 20)), int(window_height * (15 / 100)), int(window_width * (0.9) - (Data.timer * timerRatio * window_width)), int(window_width * (1 / 50))), 0))
    

Canvas.fill(white)
Canvas.blit(startimage, startimagerect)

pygame.display.flip()

if(pygame.event.poll() != pygame.NOEVENT):

    pygame.event.clear()

waitforkey()

clock = time.time()

plotter(anagselec)

Data.lnkdlist.empty()

pygame.mixer.music.play(-1, 0.0)


# Game Task Instructions

def instructions(x):

        if( x == 1 ):
            pass

        if( x == 2 ):
            selected_alpha = freq_alpha.anag_freq_alpha_selector(Data.ans, Data.ignorelist)
            copyfile("media/instruction2/" + selected_alpha + ".wav", "media/instruction2.wav")

        instruction = pygame.mixer.Sound(os.path.join(root_dir, "instruction" + str(x) +".wav"))

        return (instruction, instruction.get_length())            

# Game Task 1 - Time Reduction

def gameTask1(x):

    global clock, bgcolor, fewsecsound

    if(x):
        ##bgcolor = orange
        clock = time.time() - ((0.9) / timerRatio) * 0.80

    else:
        bgcolor = black
        fewsecsound.stop()


# Game Task 2 - Anagram with a specific alphabet 

def gameTask2(x):

    if(x):
        freq_alpha.run(Data.ans)

    else:
        for link in Data.ans:
            if(link[-1] == -1):
                link.remove(-1)
        os.remove("media/instruction2.wav")

        
# Task Handler

holdClock = clock

def Task_Handler(x):

    global Task_Deactivation_time, Next_Task_Activation_time, totalTime, clock, task_no, instruction

    if(x):
        Task_Deactivation_time = time.time() + 10#6
        Next_Task_Activation_time = (2/3) * totalTime
        instruction = None
        pygame.mixer.music.set_volume(1.0)
        exp_t1 = threading.Timer(3, Data.net_exp)
        exp_t2 = threading.Timer(6, Data.net_exp)
        exp_t3 = threading.Timer(9, Data.net_exp)
        exp_t1.start()
        exp_t2.start()
        exp_t3.start()

        t = threading.Thread(target=mousemodule.onn)##
        t.start()
          
    else:
        tend = threading.Thread(target=mousemodule.off)
        tend.start()
        Task_Deactivation_time = None
        clock = holdClock

    if(task_no == 1):
        gameTask1(x)

    if(task_no == 2):
        gameTask2(x)


# Game loop

pygame.event.set_allowed(None)
pygame.event.set_allowed([MOUSEBUTTONUP, KEYDOWN, QUIT])

instruction = None   
task_no = 0
Next_Task_Activation_time   = (1/3) * totalTime
Task_Deactivation_time = None


while True:

    # Extracting Expression Data

    inn = open("D:\\faiza\Documents\\GitHub\\Mind Canvas\\expression_output","rb")
    try:
        exp = pickle.load(inn)
        if(exp!=''):
            Data.cur_exp = exp
            Data.exp_list.append(exp)
            if( Task_Deactivation_time != None):
                Data.temp_exp_list.append(exp)
            #print(Data.cur_exp)
    except:
        pass
    inn.close()

    # Speed Check

    check_speed(dpi_speed)    
    
    # Volume Check
    
    chkvolume()

    # Giving Instructions & Activating Task
    if(int(Data.timer) == Next_Task_Activation_time and not instruction):
        pygame.mixer.music.set_volume(0.05)
        task_no += 1
        (instruction, waitTime) = instructions(task_no)
        pygame.mixer.Channel(1).play(instruction)
        t = threading.Timer(waitTime, Task_Handler, [True])
        t.start()

    # Muting Channel(0) music while instruction is being played
    if(instruction):
        pygame.mixer.Channel(0).stop()

    # Deactivating Task
    if(Task_Deactivation_time and time.time() >= Task_Deactivation_time):
        Task_Handler(False)
    
    Canvas.fill(bgcolor)

    drawtext("ANAGLINK", txtfont1, subsurface, (0.4) * window_width, window_height / 25, purple)
    drawtext("Score : " + str(Data.Score), txtfont2, subsurface, (0.8) * window_width, window_height / 25, yellow) 

    a = update_timer().width

    if(a == 1):
        Data.stat = 'Lost'
        break
    
    if(a == 100 and Data.stat == 'None'):
        fewsecsound.play(-1)
        
    if(ans == []):
        Data.stat = 'Won'
        break


    Button.pointing = 0

    Data.buttonlist.update()

    Check_playhover()

    Button.inout.clear()
    
    for event in pygame.event.get():

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                terminate()

        if event.type == QUIT :
            terminate()

        if(event.type == pygame.MOUSEBUTTONUP):
            Data.click_count += 1
            clicked()

    if(check_lnk()):
        
        pygame.mixer.Channel(0).play(linkedmusic)

        Data.Score = update_score(Data.Score, len(Data.lnkdlist), Data.stat)
        Data.buttonlist.remove(Data.lnkdlist)
        Data.lnkdlist.empty()
    
    elif(check_lnk() == False):

        Data.wrong_clicks += 1
        
        pygame.mixer.Channel(0).play(incorrectmusic)

        for l in Data.lnkdlist:
            l.active = False
            l.wrong = True
            Data.lnkdlist.empty()

    #print(Data.click_count, Data.right_clicks, Data.wrong_clicks)##
    pygame.display.flip()

pygame.mixer.music.stop()

fewsecsound.stop()

if( Data.stat == 'Lost' ):

    loosemusic.play()
    Canvas.blit(lostimage, lostimagerect)

if( Data.stat == 'Won' ):

    winmusic.play()
    Data.Score = update_score(Data.Score, Data.timer, Data.stat) 
    Canvas.blit(wonimage, wonimagerect)

pygame.display.flip()

waitforkey()

time.sleep(1)

pygame.quit()

check_speed(10)

# Leaderboard

import LeaderBoard as lb

leaderboard = lb.NewLeaderBoard("leaderboard")
leaderboard.sendData(Data.stat, Data.Score, Data.TimeBonus)

Data.release_proc()
