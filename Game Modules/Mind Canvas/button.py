from Data import *
import Data

bwidth  = 136
bheight = int(bwidth * 19 / 68)

hoversound = pygame.mixer.Sound(os.path.join(root_dir, "hover.wav"))
clicksound = pygame.mixer.Sound(os.path.join(root_dir, "click.wav"))

def clicked():

    for self in Data.buttonlist:
        if(Button.pointing == self):

            clicksound.play()


            if( not self.active ):
                self.active = True
                Data.lnkdlist.add(self)

            else:
                self.active = False
                Data.lnkdlist.remove(self)
                played = False

def check_lnk():
    
    lst = list()

    for obj in Data.lnkdlist:

        lst.append(obj.value)

    for l in lst:
        if([l] in Data.ignorelist and len(lst)>1):

            return False

    for a in Data.ans:

        if(set(a) == set(lst)):
            Data.ans.remove(a)
            return True

        elif(lst != [] and lst[0] in a):
            if(not set(lst) < set(a)):
                return False


class Button(pygame.sprite.Sprite):

    inout = []
    sound = False
    pointing = 0


    def __init__(self, surface, x, y, wrd):
        global bwidth, bheight
        pygame.sprite.Sprite.__init__(self)
        Button.surface = surface
        self.rect = pygame.Rect(x, y, bwidth, bheight)
        self.active = False
        self.gid = 0
        self.value = wrd
        self.wrong = False
        self.wait = 0
        

    def checkmouseloc(self, loc):
        
        if(loc[0] >= self.rect.left and loc[0] <= self.rect.right and loc[1] >= self.rect.top and loc[1] <= self.rect.bottom):
            Button.inout.append(1)
            Button.pointing = self
            return True
        else:
            Button.inout.append(0)
            
                
    
    def update(self):

        global wait

        if( self.wrong == True ):
            pygame.draw.rect( Button.surface, red, self.rect, 0)
            self.wait = self.wait + 1
            if(self.wait == 100):
                self.wrong = False
                self.wait = 0
        else:
            pygame.draw.rect( Button.surface, cyan, self.rect, 2)

        self.checkmouseloc(pygame.mouse.get_pos())

        if( self.active == True ):
            pygame.draw.rect( Button.surface, orange, self.rect, 0)
            pygame.draw.rect( Button.surface, orange, self.rect, 5)

        drawtext( self.value, txtfont2, Button.surface, int(self.rect.left + window_width*1/200), self.rect.top, green )

def Check_playhover():
    
    if(1 in Button.inout and Button.sound == False):
        hoversound.play()
        Button.sound = True

    elif(1 not in Button.inout):
        Button.sound = False

    if(Button.pointing != 0):
        pygame.draw.rect( Button.surface, cyan, Button.pointing.rect, 5)
