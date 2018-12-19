import loading
from Data import *
from button import *
from Scoring_Algo import *
import Data
import time
import os


# Close loading window

loading.root.destroy()


# Initializing window

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % loading.get_coord(window_width, window_height)

pygame.init()
pygame.display.set_caption("Anaglink")
Canvas = pygame.display.set_mode((window_width, window_height), pygame.HWSURFACE)

Data.foregroundWindow("Anaglink")

subsurface = Canvas.subsurface((0, 0, window_width, (1 / 5) * window_height))


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


# Timer - 60s

ratio = (0.9) / 60

def update_timer():

    global clock

    Data.timer = time.time() - clock

    pygame.draw.rect( subsurface, cyan, ( int(window_width * (1 / 20)), int(window_height * (15 / 100)), int(window_width * (0.9)), int(window_width * (1 / 50))), 2)

    return( pygame.draw.rect( subsurface, red, ( int(window_width * (1 / 20)), int(window_height * (15 / 100)), int(window_width * (0.9) - (Data.timer * ratio * window_width)), int(window_width * (1 / 50))), 0))
    

Canvas.fill(white)
Canvas.blit(startimage, startimagerect)

pygame.display.flip()

waitforkey()
waitforkey()

clock = time.time()

plotter(anagselec)

Data.lnkdlist.empty()

pygame.mixer.music.play(-1, 0.0)


# Game loop

while True:

    Canvas.fill(black)

    drawtext("ANAGLINK", txtfont1, subsurface, (0.4) * window_width, window_height / 25, purple)
    drawtext("Score : " + str(Data.Score), txtfont2, subsurface, (0.8) * window_width, window_height / 25, yellow) 


    a = update_timer().width

    if( a == 1 ):
        Data.stat = 'Lost'
        break
    
    if( a == 100 and Data.stat == 'None'):
        fewsecsound.play(-1)
        
    if( ans == [] ):
        Data.stat = 'Won'
        break


    Button.pointing = 0

    Data.buttonlist.update()

    Check_playhover()

    Button.inout.clear()

    clicked()

    if(check_lnk()):

        linkedmusic.play()

        Data.Score = update_score(Data.Score, len(Data.lnkdlist), Data.stat)
        Data.buttonlist.remove(Data.lnkdlist)
        Data.lnkdlist.empty()

    elif(check_lnk() == False):

        incorrectmusic.play()

        for l in Data.lnkdlist:
            l.active = False
            l.wrong = True
            Data.lnkdlist.empty()


    for event in pygame.event.get():

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                terminate()

        if event.type == QUIT :
            terminate()
            
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


# Leaderboard

import LeaderBoard as lb

leaderboard = lb.NewLeaderBoard("leaderboard")
leaderboard.sendData(Data.stat, Data.Score, Data.TimeBonus)
