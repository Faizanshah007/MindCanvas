from shutil import copyfile
import threading, subprocess
import loading
import pickle
import time
import cv2
import os


from Core import pygame, ANAGSCHOSEN, WINDOW_WIDTH, WINDOW_HEIGHT, ROOT_DIR, TXT_FONT_1, TXT_FONT_2
import Core


subprocess.Popen("python label.py", shell = True, cwd = os.path.abspath('.\\..\\Expression Recognition'))  # Starting Expression Recognition Module


# Loading Game

import button
import freq_alpha
import Scoring_Algo
import mousemodule


# Set Mouse DPI

dpi_speed = 8
check_speed = mousemodule.dpi(dpi_speed)


# Let the Expression Module obtain webcam control.

while True:
    loading.root.update()
    cap = cv2.VideoCapture(0)

    if(not cap.isOpened()):
        cap.release()
        break

    cap.release()

time.sleep(1)

loading.root.destroy()  # Close the loading window.


# Initializing window

os.environ['SDL_VIDEO_CENTERED'] = '1'  # Centering the pygame window
pygame.display.set_caption("Anaglink")
Canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.NOFRAME)
pygame.event.set_grab(True)
Core.foregroundWindow("Anaglink")
subsurface = Canvas.subsurface((0, 0, WINDOW_WIDTH, (1 / 5) * WINDOW_HEIGHT))


# Setting up the media

pygame.mixer.music.load(os.path.join(ROOT_DIR, "main.wav"))

loosemusic = pygame.mixer.Sound(os.path.join(ROOT_DIR, "game_over.wav"))
winmusic = pygame.mixer.Sound(os.path.join(ROOT_DIR, "winner.wav"))
linkedmusic = pygame.mixer.Sound(os.path.join(ROOT_DIR, "anaglinked.wav"))
incorrectmusic = pygame.mixer.Sound(os.path.join(ROOT_DIR, "incorrect.wav"))
fewsecsound = pygame.mixer.Sound(os.path.join(ROOT_DIR, "fewsecleft.wav"))

startimage = pygame.image.load(os.path.join(ROOT_DIR, "start.jpg"))
startimage = pygame.transform.scale( startimage, ( WINDOW_WIDTH, WINDOW_HEIGHT ) )
startimagerect = startimage.get_rect()
startimagerect.centerx = WINDOW_WIDTH / 2
startimagerect.centery = WINDOW_HEIGHT / 2

lostimage = pygame.image.load(os.path.join(ROOT_DIR, "lost.jpg"))
lostimage = pygame.transform.scale( lostimage, ( WINDOW_WIDTH, WINDOW_HEIGHT ) )
lostimagerect = startimage.get_rect()
lostimagerect.centerx = WINDOW_WIDTH / 2
lostimagerect.centery = WINDOW_HEIGHT / 2

wonimage = pygame.image.load(os.path.join(ROOT_DIR, "won.jpg"))
wonimage = pygame.transform.scale( wonimage, ( WINDOW_WIDTH, WINDOW_HEIGHT ) )
wonimagerect = startimage.get_rect()
wonimagerect.centerx = WINDOW_WIDTH / 2
wonimagerect.centery = WINDOW_HEIGHT / 2


# Button Plotting

def plotter(list_):
    for i in range(5):
        for j in range(5):
            Core.buttonlist.add( button.Button( Canvas, int(WINDOW_WIDTH * (1 / 20 + j / 5)), int(WINDOW_HEIGHT * (1 / 4 + i * 1 / 7)), list_[j + 5 * i]) )


Canvas.fill(Core.colors['WHITE'])
Canvas.blit(startimage, startimagerect)

pygame.display.flip()

if(pygame.event.poll() != pygame.NOEVENT):

    pygame.event.clear()

Core.waitforkey()


# Timer
start_time      = time.time()  # Timer starts from here (DO NOT RE-POSITION)
start_time_copy = start_time   # Used by Game Task 1
totalTime  = 60
timerRatio = (0.9) / totalTime
timerRect  = pygame.Rect(int(WINDOW_WIDTH * (1 / 20)), int(WINDOW_HEIGHT * (15 / 100)), int(WINDOW_WIDTH * (0.9)), int(WINDOW_WIDTH * (1 / 50)))

def update_timer():

    global start_time

    Core.timer = time.time() - start_time

    pygame.draw.rect(subsurface, Core.colors['CYAN'], timerRect, int(WINDOW_WIDTH / 500))

    return(pygame.draw.rect(subsurface, Core.colors['RED'], (timerRect.topleft, (int(timerRect.width - (Core.timer * timerRatio * WINDOW_WIDTH)), timerRect.height)), 0))


plotter(ANAGSCHOSEN)

Core.lnkdlist.empty()

pygame.mixer.music.play(-1, 0.0)


# Game Task Instructions

def instructions(x):

        if( x == 1 ):
            pass

        # Select an alphabet & its respective instruction as instruction2.wav
        if( x == 2 ):
            selected_alpha = freq_alpha.anag_freq_alpha_selector(Core.ans, Core.ignorelist)
            copyfile("media/instruction2/" + selected_alpha + ".wav", "media/instruction2.wav")

        instruction = pygame.mixer.Sound(os.path.join(ROOT_DIR, "instruction" + str(x) +".wav"))

        return (instruction, instruction.get_length())

# Game Task 1 - Time Reduction

def gameTask1(x):

    global start_time, fewsecsound

    if(x):
        start_time = time.time() - totalTime * 0.80

    else:
        start_time = start_time_copy
        fewsecsound.stop()

# Game Task 2 - Anagram with a specific alphabet

def gameTask2(x):

    if(x):
        freq_alpha.run(Core.ans)  # Updating valid anaglinks in ans according to the task

    else:
        # Making all anaglinks in ans valid again
        for link in Core.ans:
            if(link[-1] == -1):
                link.remove(-1)
        os.unlink("media/instruction2.wav")

##INSPECTING
# Task Handler

instruction = None
task_no = 0
Next_Task_Activation_time   = (1/3) * totalTime
Task_Deactivation_time = None

def Task_Handler(x):

    global Task_Deactivation_time, Next_Task_Activation_time, totalTime, start_time, task_no, instruction

    if(x):
        Task_Deactivation_time = time.time() + 10
        Next_Task_Activation_time = (2/3) * totalTime
        instruction = None
        pygame.mixer.music.set_volume(1.0)
        expr_t1 = threading.Timer(3, Core.net_expr)
        expr_t2 = threading.Timer(6, Core.net_expr)
        expr_t3 = threading.Timer(9, Core.net_expr)
        expr_t1.start()
        expr_t2.start()
        expr_t3.start()

        mousemodule_thread = threading.Thread(target=mousemodule.on)##
        mousemodule_thread.start()

        Core.click_count  = 0
        Core.right_clicks = 0
        Core.wrong_clicks = 0

        Core.colors['ORANGE']  = (39, 58, 89)
        Core.colors['BLACK']   = (255,255,255)
        Core.colors['CYAN']    = (0, 255, 0)


    else:
        tend = threading.Thread(target=mousemodule.off)
        tend.start()
        Task_Deactivation_time = None

        print("Clicks-",Core.click_count,Core.right_clicks,Core.wrong_clicks)

        Core.colors['ORANGE']  = (255, 165, 0)
        Core.colors['BLACK']   = (0, 0, 0)
        Core.colors['CYAN']    = (0, 255, 255)

    if(task_no == 1):
        gameTask1(x)

    if(task_no == 2):
        gameTask2(x)


# Game loop

pygame.event.set_allowed(None)
pygame.event.set_allowed([pygame.MOUSEBUTTONUP, pygame.KEYDOWN, pygame.QUIT])


while True:

    # Extracting Expression Core

    inn = open("D:\\faiza\Documents\\GitHub\\Mind Canvas\\expression_output","rb")
    try:
        expr = pickle.load(inn)
        if(expr!=''):
            Core.cur_expr = expr
            Core.expr_list.append(expr)
            if( Task_Deactivation_time != None):
                Core.temp_expr_list.append(expr)
            #print(Core.cur_expr)
    except:
        pass
    inn.close()

    # Speed Check

    check_speed(dpi_speed)

    # Volume Check

    Core.chkvolume()

    # Giving Instructions & Activating Task
    if(int(Core.timer) == Next_Task_Activation_time and not instruction):
        pygame.mixer.music.set_volume(0.05)
        task_no += 1
        (instruction, waitTime) = instructions(task_no)
        pygame.mixer.Channel(1).play(instruction)
        task_thread = threading.Timer(waitTime, Task_Handler, [True])
        task_thread.start()

    # Muting Channel(0) music while instruction is being played
    if(instruction):
        pygame.mixer.Channel(0).stop()

    # Deactivating Task
    if(Task_Deactivation_time and time.time() >= Task_Deactivation_time):
        Task_Handler(False)

    Canvas.fill(Core.bgcolor)

    Core.drawtext("ANAGLINK", TXT_FONT_1, subsurface, WINDOW_WIDTH / 2, timerRect.top / 2, Core.colors['PURPLE'])
    Core.drawtext("Score : " + str(Core.Score), TXT_FONT_2, subsurface, (259/304) * WINDOW_WIDTH, (10 / 23) * timerRect.top, Core.colors['YELLOW'])

    a = update_timer().width

    if(a == 1):
        Core.stat = 'Lost'
        break

    if(a <= 100 and Core.stat == 'None'):
        fewsecsound.play(-1)
        Core.stat = 'fewsecleft'

    if(Core.ans == []):
        Core.stat = 'Won'
        break


    button.Button.pointing = None

    Core.buttonlist.update()

    button.Check_playhover()

    button.Button.inout.clear()

    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Core.terminate()

        if event.type == pygame.QUIT :
            Core.terminate()

        if(event.type == pygame.MOUSEBUTTONUP):
            Core.click_count += 1
            button.clicked()

    if(button.check_lnk()):

        pygame.mixer.Channel(0).play(linkedmusic)

        Core.Score = Scoring_Algo.update_score(Core.Score, len(Core.lnkdlist), Core.stat)
        Core.buttonlist.remove(Core.lnkdlist)
        Core.lnkdlist.empty()

    elif(button.check_lnk() == False):

        Core.wrong_clicks += 1

        pygame.mixer.Channel(0).play(incorrectmusic)

        for item in Core.lnkdlist:
            item.active = False
            item.wrong = True
            Core.lnkdlist.empty()

    #print(Core.click_count, Core.right_clicks, Core.wrong_clicks)##
    pygame.display.flip()

pygame.mixer.music.stop()

fewsecsound.stop()

if( Core.stat == 'Lost' ):

    loosemusic.play()
    Canvas.blit(lostimage, lostimagerect)

if( Core.stat == 'Won' ):

    winmusic.play()
    Core.Score = Scoring_Algo.update_score(Core.Score, totalTime - Core.timer, Core.stat)
    Canvas.blit(wonimage, wonimagerect)

pygame.display.flip()

Core.waitforkey()

time.sleep(1)

pygame.quit()

check_speed(10)

# Leaderboard

import LeaderBoard as lb

leaderboard = lb.NewLeaderBoard("Leaderboard")
leaderboard.sendData(Core.stat, Core.Score, Core.TimeBonus)

Core.terminate()
