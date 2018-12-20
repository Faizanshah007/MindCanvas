from tkinter import *
from LeaderBoard_BackEnd import *
import LeaderBoard_BackEnd as backend
import os, sys

root = None

class LeaderBoard(Frame):

    def update(self):
        
        # Disfunction submit button until valid data entered

        if(self.ent.get() != "" and self.ent.get() != "ENTER YOUR NAME"):

            self.flag = 1
            toDatabase(self.ent.get(), self.Score, self.TimeBonus)

        # Updating scroll region

        self.cv.config(scrollregion = (0, 0, 600, 30 + 37 * (backend.count - 1)))
        
        if(self.flag == 1):

            self.flag = 0
            i = 0
            info = list()

            # Extracting and arranging leaderboard data

            while(True):

                data = getData(i + 1)

                if((data) == None):
                    break

                info.clear()

                for d in data:
                    info.append(d)
                
                self.cv.create_polygon(0, 0 + 37 * i, 600, 0 + 37 * i, 600, 30 + 37 * i, 0, 30 + 37 * i)
                    
                self.cv.create_text(30,  37 * i + 15, text = "   " + str(i + 1), fill = "white", anchor = "w", font = ("Alfie", 10))
                self.cv.create_text(82,  37 * i + 15, text = "|", anchor = "w", fill = "white", font = ("Alfie", 10))
                self.cv.create_text(100, 37 * i + 15, text = str(info[2]), anchor = "w", fill = "white", font = ("Alfie", 10), width = 250)
                self.cv.create_text(338, 37 * i + 15, text = "|             " + str(info[4]), fill = "white", anchor = "w", font = ("Alfie", 10))
                self.cv.create_text(450, 37 * i + 15, text = "|               " + str(info[3]), anchor = "w", fill = "white", font = ("Alfie", 10))

                if(i == 0 or i == 1 or i == 2):

                    r = self.cv.create_polygon(10, 8 + 37 * i, 30, 8 + 37 * i, 30, 23 + 37 * i, 10, 23 + 37 * i)

                    if(i == 0):
                        self.cv.itemconfig(r, fill = "gold")
                    if(i == 1):
                        self.cv.itemconfig(r, fill = "silver")
                    if(i == 2):
                        self.cv.itemconfig(r, fill = "#cd7f32")

                if(backend.count == info[0] and self.ent.get() != ""):

                    self.ent.delete(0, len(self.ent.get()) + 1)
                    self.ent.config(state = DISABLED)
                    self.cv.create_polygon(0, 0 + 37 * i + 2, 600, 0 + 37 * i + 2, 600, 30 + 37 * i - 2, 0, 30 + 37 * i - 2, outlinestipple = "gray50", outline = "white", fill = "", width = 7)

                    if(info[1] > 7 and info[1] < (backend.count - 2)):
                        self.cv.yview_moveto((37 * (info[1] - 5)) / ((37 * backend.count) - 7))

                    elif(info[1] >= (backend.count - 2)):
                        self.cv.yview_moveto(1.0)

                    else:
                        self.cv.yview_moveto(0.0)

                i = i + 1

    # Creating Leaderboard GUI
        
    def createBody(self):

        sp1 = Label(self.frame, bg = "black")
        sp1.grid(pady = 10, columnspan = 8) 

        l = Label(self.frame, text = "Player's Name ", bg = "black", fg = "white", font = ("Helvetica",15,"bold italic"))
        l.grid(row = 1, columnspan = 2)


        self.name = StringVar(self.frame)

        self.ent = Entry(self.frame, bd = 5, bg = "white", font = ("Uni Sans", "12", "bold italic"), textvariable = self.name, width = 48) 
        self.ent.grid(row = 1, column = 3)

        def to_uppercase(*args):
            self.name.set(self.name.get().upper())

        def limit(*args):
            txt = self.name.get()
            if(len(txt) > 27):
                self.name.set(txt[:27])

        try:
            # python 3.6
            self.name.trace_add('write', to_uppercase)
            self.name.trace_add('write', limit)
        except AttributeError:
            # python < 3.6
            self.name.trace('w', to_uppercase)
            self.name.trace_add('w', limit)
            
            
        bt = Button(self.frame, activebackground = "#4D4D4D", text = "Submit", bg = "#808080", command = self.update, relief = GROOVE, font = ("Jokerman", 12), width = 10)
        bt.grid(column = 3, sticky = "NE", pady = 9)

        self.ent.bind("<Return>", lambda event: self.update())

        self.subframe = Frame(self.frame, bg = "#87cefa", height = 300)
        self.subframe.grid(columnspan = 8, column = 0, row = 6, rowspan = 3, sticky = "W")

        heading = LabelFrame(self.subframe, bg = "#87cefa", height = 30, width = 620)
        heading.grid(row = 0, column = 0, columnspan = 20, sticky = "w")

        l1 = Label(heading, bg = "#1e90ff", text = "     RANK   ", anchor = "w", font = ('times', 11, 'bold'))
        l1.grid(row = 0, column = 0, sticky = "W")
        l2 = Label(heading, bg = "#1e90ff", text = "                           NAME                            ", anchor = "w", font = ('times', 11, 'bold'))
        l2.grid(row = 0, column = 1, sticky = "W",columnspan = 1)
        l3 = Label(heading, bg = "#1e90ff", text = "   BONUS           ", anchor = "w", font = ('times', 11, 'bold'))
        l3.grid(row = 0, column = 5, sticky = "W")
        l4 = Label(heading, bg = "#1e90ff", text = "    SCORE                  ", anchor = "w", font = ('times', 11, 'bold'))
        l4.grid(row = 0, column = 7, sticky = "W")
        
        self.cv = Canvas(self.subframe, bg = "#87cefa", height = 300, width = 600)
        self.cv.grid( columnspan = 8, column = 0, row = 1, rowspan = 6, sticky = "W")

        self.frame.bind("<Up>", lambda event: self.cv.yview_scroll(-1, "units"))
        self.frame.bind("<Down>", lambda event: self.cv.yview_scroll(1, "units"))
        self.frame.bind("<Prior>", lambda event: self.cv.yview_scroll(-1, "pages"))
        self.frame.bind("<Next>", lambda event: self.cv.yview_scroll(1, "pages"))
        
        self.vsb = Scrollbar(self.subframe)
        self.vsb.grid(column = 8, row = 1, rowspan = 6, ipady = 127, sticky = "SE")

        self.hyplnk = Button(self.subframe, bg = "#808080", fg = "white", font = ("Jokerman", 12, "underline"), activebackground = "#87cefa", relief = FLAT, text = "Generate Summary", command = self.gensum)
        self.hyplnk.grid(row = 7, columnspan = 20)

        self.vsb.config( command = self.cv.yview)
        self.cv.config(yscrollcommand = self.vsb.set)

        self.flag = 1
        self.update()

    def __init__(self, master = None):

        self.frame = root
        self.frame.config(bg = "black")
        self.Score = 0
        self.TimeBonus = 0
        self.flag = 0
        self.createBody()

    # Commands for widgets

    def gensum(self):

        self.hyplnk.config(text = "Generating Summary......")
        self.frame.update()

        import Summary_Generator

        Summary_Generator.runweb()

        self.hyplnk.config(text = "Generate Summary")
        self.frame.update()

    def initial_reset(self, *args):

        if(self.ent.get() == "ENTER YOUR NAME"):

            self.ent.delete(0, len(self.ent.get()) + 1)
            self.ent.config(fg = "black")


    # Recieving data from user
    
    def sendData(self, st, sc, tb):

        global root

        self.player_status = st

        if(self.player_status == 'Lost'):

            self.ent.config(state=DISABLED)
            
        elif(self.player_status == 'Won'):

            self.ent.config(self.name.set("ENTER YOUR NAME"), fg = "#a6a6a6")
            self.ent.bind("<1>", self.initial_reset)

        self.Score = sc
        self.TimeBonus = tb

        root.mainloop()


# Function to generate new leaderboard object

def NewLeaderBoard(nm):

    global root

    establishConnection(nm)

    root = Tk(className = " Leader Board ")
    root.resizable(0,0)
    obj = LeaderBoard(master=root)
    root.protocol("WM_DELETE_WINDOW",root.destroy)

    return obj
