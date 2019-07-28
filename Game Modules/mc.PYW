from shutil import copyfile
## from rprint import print  # Use this version of print whenever testing any module
import threading, subprocess
import loading
import pickle
import time
import os

## import atexit
## atexit.register(print,"Exiting mc")

from Core import pygame, ANAGSCHOSEN, WINDOW_WIDTH, WINDOW_HEIGHT, MEDIA_DIR, TXT_FONT_1, TXT_FONT_2, mousemodule
import Core

subprocess.call("setx OPENCV_VIDEOIO_PRIORITY_MSMF 0")  # Workaround for an OpenCV bug
subprocess.Popen("python label.py", shell = True, cwd = os.path.abspath('.\\..\\Expression Recognition'))  # Starting Expression Recognition Module


# Loading Game

import button
import freq_alpha
import Scoring_Algo


# Let the Expression Module obtain webcam control.

while True:
    loading.root.update()
    try:
        Cond_f = open(".\\..\\switch","rb")

        if(pickle.load(Cond_f) == "on"):
            Cond_f.close()
            break

        Cond_f.close()

    except:
        pass

time.sleep(1)

loading.root.destroy()  # Close the loading window.


# Initializing window

os.environ['SDL_VIDEO_CENTERED'] = '1'  # Centering the pygame window
pygame.display.set_caption("Anaglink")
Canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.NOFRAME)
subsurface = Canvas.subsurface((0, 0, WINDOW_WIDTH, (1 / 5) * WINDOW_HEIGHT))


# Setting up the media

pygame.mixer.music.load(os.path.join(MEDIA_DIR, "main.wav"))

loosemusic = pygame.mixer.Sound(os.path.join(MEDIA_DIR, "game_over.wav"))
winmusic = pygame.mixer.Sound(os.path.join(MEDIA_DIR, "winner.wav"))
linkedmusic = pygame.mixer.Sound(os.path.join(MEDIA_DIR, "anaglinked.wav"))
incorrectmusic = pygame.mixer.Sound(os.path.join(MEDIA_DIR, "incorrect.wav"))
fewsecsound = pygame.mixer.Sound(os.path.join(MEDIA_DIR, "fewsecleft.wav"))

startimage = pygame.image.load(os.path.join(MEDIA_DIR, "start.jpg"))
startimage = pygame.transform.scale( startimage, ( WINDOW_WIDTH, WINDOW_HEIGHT ) )
startimagerect = startimage.get_rect()
startimagerect.centerx = WINDOW_WIDTH / 2
startimagerect.centery = WINDOW_HEIGHT / 2

lostimage = pygame.image.load(os.path.join(MEDIA_DIR, "lost.jpg"))
lostimage = pygame.transform.scale( lostimage, ( WINDOW_WIDTH, WINDOW_HEIGHT ) )
lostimagerect = startimage.get_rect()
lostimagerect.centerx = WINDOW_WIDTH / 2
lostimagerect.centery = WINDOW_HEIGHT / 2

wonimage = pygame.image.load(os.path.join(MEDIA_DIR, "won.jpg"))
wonimage = pygame.transform.scale( wonimage, ( WINDOW_WIDTH, WINDOW_HEIGHT ) )
wonimagerect = startimage.get_rect()
wonimagerect.centerx = WINDOW_WIDTH / 2
wonimagerect.centery = WINDOW_HEIGHT / 2


# Button Plotting

def plotter(list_):
    for i in range(5):
        for j in range(5):
            Core.buttonlist.add( button.Button( Canvas, int(WINDOW_WIDTH * (4 / 125 + j / 5)), int(WINDOW_HEIGHT * (1 / 4 + i * 1 / 7)), list_[j + 5 * i]) )


Canvas.fill(Core.colors['WHITE'])
Canvas.blit(startimage, startimagerect)

pygame.display.flip()


# Continuously try to foreground the game window
while(not Core.foregroundWindow(os.getpid())):
    pass
pygame.event.set_grab(True)

## Explain this
if(pygame.event.poll() != pygame.NOEVENT):

    pygame.event.clear()

Core.waitforkey()


# Timer
start_time      = time.time()  # Timer starts from here (DO NOT RE-POSITION)
start_time_copy = start_time   # Used by Game Task 1
timerRatio = (0.9) / Core.TOTAL_TIME
timerRect  = pygame.Rect(0, int(WINDOW_HEIGHT * (15 / 100)), int(WINDOW_WIDTH * (0.9)), int(WINDOW_WIDTH * (1 / 50)))
timerRect.centerx = int(WINDOW_WIDTH / 2)

def update_timer():

    global start_time

    Core.timer = time.time() - start_time

    pygame.draw.rect(subsurface, Core.colors['BLUE_VARIANT_1'], timerRect, int(WINDOW_WIDTH / 500))

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

        instruction = pygame.mixer.Sound(os.path.join(MEDIA_DIR, "instruction" + str(x) +".wav"))

        return (instruction, instruction.get_length())

# Game Task 1 - Time Reduction

def gameTask1(x):

    global start_time, fewsecsound

    if(x):
        start_time = time.time() - Core.TOTAL_TIME * 0.80

    else:
        start_time = start_time_copy
        fewsecsound.stop()
        Core.stat = 'None'

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


# Task Handler

instruction = None
task_no = 0
Next_Task_Activation_time   = (1/3) * Core.TOTAL_TIME
Task_Deactivation_time = None
task_handler_start_time = None

def Task_Handler(x):

    global Task_Deactivation_time, Next_Task_Activation_time, instruction, timer_thread_1, timer_thread_2, timer_thread_3, mousemodule_on_thread_2

    if(x):

        # Bring back the volume of the sounds since the instruction is over
        for i in range(1,5):
            pygame.mixer.Channel(i).set_volume(1.0)

        Task_Deactivation_time = time.time() + 10  # Duration of any task is 10 seconds
        Next_Task_Activation_time = ((task_no + 1)/3) * Core.TOTAL_TIME
        #instruction = None
        pygame.mixer.music.set_volume(1.0)
        # Capture & filter out 3 prominent expressions throught the task
        timer_thread_1 = threading.Timer(3, Core.net_expr)
        timer_thread_1.start()
        timer_thread_2 = threading.Timer(6, Core.net_expr)
        timer_thread_2.start()
        timer_thread_3 = threading.Timer(9, Core.net_expr)
        timer_thread_3.start()

        mousemodule_on_thread_2 = threading.Thread(target=mousemodule.on)
        mousemodule_on_thread_2.start()

        Core.click_count  = 0
        Core.button_clicks = 0
        Core.wrong_clicks = 0

        Core.colors['BLUE']                = (39, 58, 89)
        Core.colors['BLACK']               = (255,255,255)
        Core.colors['BLUE_VARIANT_1']      = (0, 255, 0)


    else:
        mousemodule.off()
        Task_Deactivation_time = None
        instruction = None

        Core.colors['BLUE']                = (0, 0, 255)
        Core.colors['BLACK']               = (0, 0, 0)
        Core.colors['BLUE_VARIANT_1']      = (0, 110, 255)

        # Wait until all the results are ready
        timer_thread_1.join()
        timer_thread_2.join()
        timer_thread_3.join()
        mousemodule_on_thread_2.join()

        ## Storing MindCanvas's final result data into a file, Which will be used by k-means module
        result_file = open("Result.txt","a")
        result_file.write(str(tuple((tuple(Core.selected_exprs), Core.players_initial_avg_speed - mousemodule.return_avg_speed(), (Core.button_clicks - Core.wrong_clicks), Core.wrong_clicks, (Core.click_count - Core.button_clicks)))) + "\n")
        result_file.close()

        Core.selected_exprs.clear()

    if(task_no == 1):
        gameTask1(x)

    if(task_no == 2):
        gameTask2(x)


# Set Mouse DPI

dpi_speed = 4
set_mouse_dpi = Core.set_dpi(dpi_speed)


# Game loop
## Explain sound channel allotments

pygame.event.set_blocked(None)  # Block all events
pygame.event.set_allowed([pygame.MOUSEBUTTONUP, pygame.KEYDOWN, pygame.QUIT])  # Unblock specific events for faster game flow

Core.stat = "Recording player's initial avg speed"
mousemodule_on_thread_1 = threading.Thread(target=mousemodule.on)
mousemodule_on_thread_1.start()

Core.volume.SetMasterVolumeLevel(-11.8, None)  # Set initial volume at 45%

while True:

    # Extracting Expression
    Core.cur_expr = ''  # Reset
    expr_in = open(".\\..\\expression_output","rb")
    try:
        expr_tuple = pickle.load(expr_in)
        Core.cur_expr = expr_tuple
        Core.expr_list.append(expr_tuple[0])
        if( Task_Deactivation_time != None):
            Core.task_expr_list.append(expr_tuple)
        ## print(Core.cur_expr)
    except:
        pass
    expr_in.close()

    # Speed Check
    set_mouse_dpi(dpi_speed)

    # Volume Check

    Core.check_volume()

    # Player's initial avg speed calculation
    ## Explain with comments

    if(Core.stat == "Recording player's initial avg speed"):
        if(Core.timer >= Core.players_initial_avg_speed_capture_time):
            mousemodule.off()
            Core.stat = "None"
            mousemodule_on_thread_1.join()
            Core.players_initial_avg_speed = mousemodule.return_avg_speed()

    # Giving Instructions & Activating Task
    if(Core.timer >= Next_Task_Activation_time and not instruction):
        pygame.mixer.music.set_volume(0.05)
        task_no += 1
        (instruction, waitTime) = instructions(task_no)

        # Mute other sounds to hear the instruction distinctively
        for i in range(1,5):
            pygame.mixer.Channel(i).set_volume(0.0)

        pygame.mixer.Channel(0).play(instruction)
        task_handler_start_time = time.time() + waitTime

    if(task_handler_start_time and time.time() >= task_handler_start_time):
        Task_Handler(True)
        task_handler_start_time = None

    # Deactivating Task
    if(Task_Deactivation_time and time.time() >= Task_Deactivation_time):
        Task_Handler(False)

    Canvas.fill(Core.bgcolor)

    Core.drawtext("ANAGLINK", TXT_FONT_1, subsurface, WINDOW_WIDTH / 2, timerRect.top / 2, Core.colors['PURPLE'])
    Core.drawtext("Score : " + str(Core.Score), TXT_FONT_2, subsurface, (259/304) * WINDOW_WIDTH, (10 / 23) * timerRect.top, Core.colors['YELLOW'])

    time_bar = update_timer().width

    if(time_bar == 1):
        Core.stat = 'Lost'
        break

    if(time_bar <= 100 and Core.stat != 'fewsecleft'):
        pygame.mixer.Channel(5).play(fewsecsound, -1)
        Core.stat = 'fewsecleft'

    # All the answers have been found
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

        if(event.type == pygame.MOUSEBUTTONUP):
            Core.click_count += 1
            button.clicked()

    if(button.check_lnk()):

        pygame.mixer.Channel(3).play(linkedmusic)

        Core.Score = Scoring_Algo.update_score(Core.Score, len(Core.lnkdlist), Core.stat)

        Core.buttonlist.remove(Core.lnkdlist)
        Core.lnkdlist.empty()

    elif(button.check_lnk() == False):  # Since check_lnk() also returns None when a partial anaglink is present
        Core.wrong_clicks += 1

        pygame.mixer.Channel(4).play(incorrectmusic)

        for item in Core.lnkdlist:
            item.active = False
            item.wrong = True

        Core.lnkdlist.empty()

    pygame.display.flip()

pygame.mixer.music.stop()

fewsecsound.stop()

if( Core.stat == 'Lost' ):

    loosemusic.play()
    Canvas.blit(lostimage, lostimagerect)

if( Core.stat == 'Won' ):

    winmusic.play()
    Core.Score = Scoring_Algo.update_score(Core.Score, Core.TOTAL_TIME - Core.timer, Core.stat)
    Canvas.blit(wonimage, wonimagerect)

pygame.display.flip()

Core.waitforkey()

time.sleep(1)

pygame.quit()

set_mouse_dpi(10)

# Leaderboard

import LeaderBoard as lb

leaderboard = lb.NewLeaderBoard("Leaderboard")
leaderboard.sendData(Core.stat, Core.Score, Core.TimeBonus)

## Storing the percentage value of expressions throughout the game into the result file
result_file = open("Result.txt","a")


for expr in set(Core.expr_list):
    result_file.write(expr + " -> " + str((Core.expr_list.count(expr) / len(Core.expr_list)) * 100) + "\n")


result_file.close()

Core.terminate()
