from Core import pygame, ROOT_DIR, TXT_FONT_2, WINDOW_WIDTH
import Core
import os


# Button Dimensions
bwidth  = int(WINDOW_WIDTH * 136 / 1000)
bheight = int(bwidth * 19 / 68)

hoversound = pygame.mixer.Sound(os.path.join(ROOT_DIR, "hover.wav"))
clicksound = pygame.mixer.Sound(os.path.join(ROOT_DIR, "click.wav"))


def clicked():
    for self in Core.buttonlist:

        if(Button.pointing == self):
            pygame.mixer.Channel(0).play(clicksound)

            if( not self.active ):
                self.active = True
                Core.lnkdlist.add(self)

            else:
                self.active = False
                Core.lnkdlist.remove(self)
                played = False

            Core.right_clicks += 1


def check_lnk():
    list_ = list()

    for obj in Core.lnkdlist:
        list_.append(obj.value)

    for item in list_:
        if([item] in Core.ignorelist and len(list_)>1):
            return False

    for anaglink in Core.ans:

        if(set(anaglink) == set(list_)):
            Core.ans.remove(anaglink)
            return True

        elif(list_ != [] and list_[0] in anaglink):

            if(not set(list_) < set(anaglink)):
                return False

            elif(set(list_) == set(anaglink[:-1]) and anaglink[-1] == -1):  #Task 2 special condition (-1 is appended at the last of every invalid anaglink)
                return False


class Button(pygame.sprite.Sprite):

    inout = []  # Check for mouse hover
    sound = False  # Hover sound
    pointing = None  # Button at which mouse is pointing to


    def __init__(self, surface, x, y, wrd):
        global bwidth, bheight
        pygame.sprite.Sprite.__init__(self)
        Button.surface = surface
        self.rect = pygame.Rect(x, y, bwidth, bheight)
        self.active = False
        self.value = wrd
        self.wrong = False
        self.wait = 0  # For added display lag


    def checkmouseloc(self, loc):

        if(loc[0] >= self.rect.left and loc[0] <= self.rect.right and loc[1] >= self.rect.top and loc[1] <= self.rect.bottom):
            Button.inout.append(1)
            Button.pointing = self
            return True

        else:
            Button.inout.append(0)


    def update(self):

        if( self.wrong == True ):
            pygame.draw.rect( Button.surface, Core.colors['RED'], self.rect, 0)
            self.wait = self.wait + 1

            if(self.wait == 100):
                self.wrong = False
                self.wait = 0

        else:
            pygame.draw.rect( Button.surface, Core.colors['CYAN'], self.rect, int(WINDOW_WIDTH / 500))

        self.checkmouseloc(pygame.mouse.get_pos())

        if( self.active == True ):
            pygame.draw.rect( Button.surface, Core.colors['SKY_BLUE'], self.rect, 0) ## CHANGE COLOR
            pygame.draw.rect( Button.surface, Core.colors['SKY_BLUE'], self.rect, int(WINDOW_WIDTH / 200))

        Core.drawtext( self.value, TXT_FONT_2, Button.surface, self.rect.centerx, self.rect.centery, Core.colors['GREEN'] )


def Check_playhover():

    if(1 in Button.inout and Button.sound == False):
        pygame.mixer.Channel(0).play(hoversound)
        Button.sound = True

    elif(1 not in Button.inout):
        Button.sound = False

    if(Button.pointing != None):
        pygame.draw.rect( Button.surface, Core.colors['CYAN'], Button.pointing.rect, int(WINDOW_WIDTH / 200))
