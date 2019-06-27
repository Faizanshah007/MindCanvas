from win32api import GetSystemMetrics
from PIL import Image, ImageTk
#from rprint import print
import threading
import Pre_setup
import tkinter
import sys, os


ws = GetSystemMetrics(0) # width of the screen
hs = GetSystemMetrics(1) # height of the screen


# Center align screen
def get_coord(w,h):
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    return(int(x), int(y))

# Initialize tkinter window
root = tkinter.Tk()
w = int((741/1536) * ws)
h = int((410/864) * hs)
(x, y) = get_coord(w, h)
root.geometry('%dx%d+%d+%d' % (w, h, x, y))
root.overrideredirect(True)

# Load images
loading_image = list()

for i in range(7):
    image = Image.open(os.path.join(os.path.dirname(sys.argv[0]), 'Media', str(i) + '.png'))
    image = image.resize((w, h), Image.ANTIALIAS)
    loading_image.append(ImageTk.PhotoImage(image))

# Create thread object, targeting function prepare (Consumes most of the loading time)
thread1 = threading.Thread(target=Pre_setup.prepare, args=())


# Function to update loading status
def update_stat(loading_window, loading_status):
    loading_window.config(image = loading_image[int(loading_status//20)])


# Quit loading
def quit(loading_window):
    loading_window.config(image = loading_image[6])
    root.update()
    root.quit()


# Function to check state of thread1 and to update progressbar
def progress(thread):
    thread.start()
    loading_window = tkinter.Label(root, image = loading_image[0])
    loading_window.grid()

    while thread.isAlive():
        update_stat(loading_window, Pre_setup.loaded)
        root.update()

    root.after(0, quit, loading_window)

progress(thread1)
root.mainloop()
