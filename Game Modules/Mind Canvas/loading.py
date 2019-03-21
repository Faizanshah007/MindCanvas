from tkinter import *
from PIL import Image, ImageTk
from win32api import GetSystemMetrics
import threading
import Pre_setup
import sys, os


# Center align screen

def get_coord(w,h):

    ws = GetSystemMetrics(0) # width of the screen
    hs = GetSystemMetrics(1) # height of the screen

    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    return(x, y)

# Initialize tkinter window

root = Tk()

w = 741
h = 410

(x, y) = get_coord(w, h)

root.geometry('%dx%d+%d+%d' % (w, h, x, y))

root.overrideredirect(True)

# Load images

loading_image = list()

for i in range(7):
    image = Image.open(os.path.join(os.path.dirname(sys.argv[0]), 'Media', str(i) + '.png'))
    image = image.resize((741, 410), Image.ANTIALIAS)  
    loading_image.append(ImageTk.PhotoImage(image))


# Create thread object, targeting function prepare

thread1 = threading.Thread(target=Pre_setup.prepare, args=())


# Function to update loading status

def update_stat(ld, st):

    ld.config(image = loading_image[int(st//20)])


# Quit loading

def quit(ld):

    global root

    ld.config(image = loading_image[6])
    root.update()
    root.quit()


# Function to check state of thread1 and to update progressbar

def progress(thread):

    # starts thread #
    thread.start()

    ld = Label(root, image = loading_image[0])
    ld.grid()

    # checks whether thread is alive
    while thread.is_alive():
        update_stat(ld, Pre_setup.loaded)
        root.update()

    root.after(0, quit, ld)

progress(thread1)

root.mainloop()
