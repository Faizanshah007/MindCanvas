from win32api import GetSystemMetrics
from LeaderBoard_BackEnd import *
import LeaderBoard_BackEnd as backend
import tkinter as tk
import os, sys


window_width = GetSystemMetrics(0)

lb_width = int(window_width * (620 / 1536))
lb_height = int(lb_width * (476 / 620))

root = None


class LeaderBoard(tk.Frame):

    def update(self):
        
        # Disfunction submit button until valid data entered

        if(self.name_entry.get() != "" and self.name_entry.get() != "ENTER YOUR NAME"):

            self.flag = 1
            toDatabase(self.name_entry.get(), self.Score, self.TimeBonus)

        # Updating scroll region

        self.lb_rankings.config(scrollregion = (0, 0, 0, int(self.lb_entry_height + self.lb_entry_tot_height * (backend.count - 1))))        

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
                
                self.lb_rankings.create_polygon(0, 0 + self.lb_entry_tot_height * i, self.lb_rankings.winfo_width(), 0 + self.lb_entry_tot_height * i, self.lb_rankings.winfo_width(), self.lb_entry_height + self.lb_entry_tot_height * i, 0, self.lb_entry_height + self.lb_entry_tot_height * i)
                        
                self.lb_rankings.create_text(int(self.lb_rankings.winfo_width() * (40 / 602)),  self.lb_entry_tot_height * i + int(self.lb_entry_height / 2), text = str(i + 1), fill = "white", anchor = "w", font = ("Alfie", int(self.lb_entry_height / 3)))
                self.lb_rankings.create_text(int(self.lb_rankings.winfo_width() * (82 / 602)),  self.lb_entry_tot_height * i + int(self.lb_entry_height / 2), text = "|", anchor = "w", fill = "white", font = ("Alfie", int(self.lb_entry_height / 3)))
                self.lb_rankings.create_text(int(self.lb_rankings.winfo_width() * (100 / 602)), self.lb_entry_tot_height * i + int(self.lb_entry_height / 2), text = str(info[2]), anchor = "w", fill = "white", font = ("Alfie", int(self.lb_entry_height / 3)), width = int(self.lb_rankings.winfo_width() * (250 / 602)))
                self.lb_rankings.create_text(int(self.lb_rankings.winfo_width() * (338 / 602)), self.lb_entry_tot_height * i + int(self.lb_entry_height / 2), text = "|", fill = "white", anchor = "w", font = ("Alfie", int(self.lb_entry_height / 3)))
                self.lb_rankings.create_text(int(self.lb_rankings.winfo_width() * (390 / 602)), self.lb_entry_tot_height * i + int(self.lb_entry_height / 2), text = str(info[4]), fill = "white", anchor = "w", font = ("Alfie", int(self.lb_entry_height / 3)))
                self.lb_rankings.create_text(int(self.lb_rankings.winfo_width() * (450 / 602)), self.lb_entry_tot_height * i + int(self.lb_entry_height / 2), text = "|", anchor = "w", fill = "white", font = ("Alfie", int(self.lb_entry_height / 3)))
                self.lb_rankings.create_text(int(self.lb_rankings.winfo_width() * (515 / 602)), self.lb_entry_tot_height * i + int(self.lb_entry_height / 2), text = str(info[3]), anchor = "w", fill = "white", font = ("Alfie", int(self.lb_entry_height / 3)))

                if(i == 0 or i == 1 or i == 2):

                    lb_top_rankers_emblem = self.lb_rankings.create_polygon(int(self.lb_rankings.winfo_width() * (10 / 602)), self.lb_entry_separating_border_height + self.lb_entry_tot_height * i,
                                                                            int(self.lb_rankings.winfo_width() * (30 / 602)), self.lb_entry_separating_border_height + self.lb_entry_tot_height * i,
                                                                            int(self.lb_rankings.winfo_width() * (30 / 602)), self.lb_entry_height - self.lb_entry_separating_border_height + self.lb_entry_tot_height * i,
                                                                            int(self.lb_rankings.winfo_width() * (10 / 602)), self.lb_entry_height - self.lb_entry_separating_border_height + self.lb_entry_tot_height * i)

                    if(i == 0):
                        self.lb_rankings.itemconfig(lb_top_rankers_emblem, fill = "gold")
                    if(i == 1):
                        self.lb_rankings.itemconfig(lb_top_rankers_emblem, fill = "silver")
                    if(i == 2):
                        self.lb_rankings.itemconfig(lb_top_rankers_emblem, fill = "#cd7f32")

                # Highlight current entry
                
                if(backend.count == info[0] and self.name_entry.get() != ""):

                    self.name_entry.delete(0, len(self.name_entry.get()) + 1)
                    self.name_entry.config(state = tk.DISABLED)
                    self.lb_rankings.create_polygon(0, 0 + self.lb_entry_tot_height * i + int(self.lb_rankings.winfo_height() * (2 / 295)),
                                                    self.lb_rankings.winfo_width(), 0 + self.lb_entry_tot_height * i + int(self.lb_rankings.winfo_height() * (2 / 295)),
                                                    self.lb_rankings.winfo_width(), self.lb_entry_height + self.lb_entry_tot_height * i - int(self.lb_rankings.winfo_height() * (2 / 295)),
                                                    0, self.lb_entry_height + self.lb_entry_tot_height * i - int(self.lb_rankings.winfo_height() * (2 / 295)), outlinestipple = "gray50", outline = "white", fill = "", width = int(self.lb_rankings.winfo_height() * (7 / 295)))

                    if(info[1] > 7 and info[1] < (backend.count - 2)):
                        self.lb_rankings.yview_moveto((self.lb_entry_tot_height * (info[1] - 5)) / ((self.lb_entry_tot_height * backend.count) - 7))

                    elif(info[1] >= (backend.count - 2)):
                        self.lb_rankings.yview_moveto(1.0)

                    else:
                        self.lb_rankings.yview_moveto(0.0)

                i = i + 1

    # Creating Leaderboard GUI
        
    def createBody(self):

        self.section_1 = tk.Frame(self.root, bg = "black", height = int(lb_height * (111 / 476)), width = lb_width)
        self.section_1.place(x = 0, y = 0)
        self.root.update()

        self.name_entry_label = tk.Label(self.section_1, text = "Player's Name ", bg = "black", fg = "white", font = ("Helvetica",int(self.section_1.winfo_height() * (15 / 110)),"bold italic"))
        self.name_entry_label.place(x = 0, y = int(self.section_1.winfo_height() * 0.2))
        self.root.update()

        self.name = tk.StringVar(self.root)  # Tkinter's string variable

        self.name_entry = tk.Entry(self.section_1, bd = int(self.section_1.winfo_height() * (5 / 110)), bg = "white", font = ("Uni Sans", int(self.section_1.winfo_height() * (12 / 110)), "bold italic"), textvariable = self.name) 
        self.name_entry.place(x = int(self.name_entry_label.winfo_width() + self.section_1.winfo_width() * 0.01), y = self.name_entry_label.winfo_y(), width = int(self.section_1.winfo_width() * 0.97 - self.name_entry_label.winfo_width()))
        self.root.update()
        
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
            
        self.submit_button = tk.Button(self.section_1, activebackground = "#4D4D4D", command = self.update, text = "Submit", bg = "#808080", relief = tk.GROOVE, font = ("Jokerman", int(self.section_1.winfo_height() * (12 / 110))))
        self.submit_button.place(x = int(self.section_1.winfo_width() * 0.805), y = int(self.section_1.winfo_height() * 0.55), width = int(self.section_1.winfo_width() * 0.175))
        self.root.update()
        
        self.name_entry.bind("<Return>", lambda event: self.update())

        self.section_2 = tk.Frame(self.root, bg = "#1e90ff", height = int(lb_height * (26 / 476)), width = lb_width)
        self.section_2.place(x = 0, y = self.section_1.winfo_y() + self.section_1.winfo_height())
        self.root.update()


        self.lb_heading_1 = tk.Label(self.section_2, bd = int(self.section_2.winfo_height() * (4 / 26)), bg = "#1e90ff", text = "RANK", font = ('times', int(self.section_2.winfo_height() * (11 / 26)), 'bold'))
        self.lb_heading_1.place(x = int(self.section_2.winfo_width() * (16 / 602)), y = 0)

        self.lb_heading_2 = tk.Label(self.section_2, bd = int(self.section_2.winfo_height() * (4 / 26)), bg = "#1e90ff", text = "NAME", font = ('times', int(self.section_2.winfo_height() * (11 / 26)), 'bold'))
        self.lb_heading_2.place(x = int(self.section_2.winfo_width() * (170 / 602)), y = 0)

        self.lb_heading_3 = tk.Label(self.section_2, bd = int(self.section_2.winfo_height() * (4 / 26)), bg = "#1e90ff", text = "BONUS", font = ('times', int(self.section_2.winfo_height() * (11 / 26)), 'bold'))
        self.lb_heading_3.place(x = int(self.section_2.winfo_width() * (355 / 602)), y = 0)

        self.lb_heading_4 = tk.Label(self.section_2, bd = int(self.section_2.winfo_height() * (4 / 26)), bg = "#1e90ff", text = "SCORE", font = ('times', int(self.section_2.winfo_height() * (11 / 26)), 'bold'))
        self.lb_heading_4.place(x = int(self.section_2.winfo_width() * (480 / 602)), y = 0)


        self.section_3 = tk.Frame(root, bg = "white", height = int(lb_height * (296 / 476)), width = lb_width)
        self.section_3.place(x = 0, y = self.section_2.winfo_y() + self.section_2.winfo_height())
        self.root.update()

        self.lb_rankings = tk.Canvas(self.section_3, bg = "#87cefa", height = int(self.section_3.winfo_height() * 0.985), width = int(self.section_3.winfo_width() * 0.965))
        self.lb_rankings.place(x = 0, y = 0)
        self.root.update()

        self.lb_entry_height = int(self.lb_rankings.winfo_height() * (30 / 295))
        self.lb_entry_separating_border_height = int(self.lb_rankings.winfo_height() * (7 / 295))
        self.lb_entry_tot_height = self.lb_entry_height + self.lb_entry_separating_border_height

        self.lb_scrollbar = tk.Scrollbar(self.section_3, width = self.section_3.winfo_width() - self.lb_rankings.winfo_width())
        self.lb_scrollbar.place(x = self.lb_rankings.winfo_width(), y = 0, height = self.section_3.winfo_height())
        self.root.update()

        self.root.bind("<Up>", lambda event: self.lb_rankings.yview_scroll(-1, "units"))
        self.root.bind("<Down>", lambda event: self.lb_rankings.yview_scroll(1, "units"))
        self.root.bind("<Prior>", lambda event: self.lb_rankings.yview_scroll(-1, "pages"))
        self.root.bind("<Next>", lambda event: self.lb_rankings.yview_scroll(1, "pages"))

        #Source: https://stackoverflow.com/questions/17355902/python-tkinter-binding-mousewheel-to-scrollbar
        def _on_mousewheel(event):
            self.lb_rankings.yview_scroll(int(-1*(event.delta/120)), "units")
            
        self.root.bind("<MouseWheel>", _on_mousewheel)

        self.lb_scrollbar.config( command = self.lb_rankings.yview)
        self.lb_rankings.config(yscrollcommand = self.lb_scrollbar.set)
        self.lb_rankings.yview_moveto(0.0)  # Resolves a scroll region glitch

        self.section_4 = tk.Frame(self.root, bg = "#87cefa", height = int(lb_height * (45 / 476)), width = lb_width)
        self.section_4.place(x = 0, y = self.section_3.winfo_y() + self.section_3.winfo_height())
        self.root.update()

        self.summary_button = tk.Button(self.section_4, bg = "#808080", fg = "white", font = ("Jokerman", int(self.section_4.winfo_height() * (13 / 45)), "underline"), activebackground = "#87cefa", relief = tk.FLAT, text = "Generate Summary", command = self.gensum)
        self.summary_button.place(x = int(self.section_4.winfo_width() * 0.354), y = 0, height = self.section_4.winfo_height())
        self.root.update()

        self.flag = 1

        self.update()


    def __init__(self, master = None):

        self.root = master
        self.root.config(width = lb_width, height = lb_height)
        self.Score = 0
        self.TimeBonus = 0
        self.flag = 0
        self.createBody()

    # Commands for widgets

    def gensum(self):

        self.summary_button.config(text = "Generating Summary......")
        self.root.update()

        import Summary_Generator

        Summary_Generator.runweb()

        self.summary_button.config(text = "Generate Summary")
        self.root.update()

    def initial_reset(self, *args):

        if(self.name_entry.get() == "ENTER YOUR NAME"):

            self.name_entry.delete(0, len(self.name_entry.get()) + 1)
            self.name_entry.config(fg = "black")


    # Recieving data from user
    
    def sendData(self, st, sc, tb):

        self.player_status = st

        if(self.player_status == 'Lost'):

            self.name_entry.config(state=tk.DISABLED)
            
        elif(self.player_status == 'Won'):

            self.name_entry.config(self.name.set("ENTER YOUR NAME"), fg = "#a6a6a6")
            self.name_entry.bind("<1>", self.initial_reset)

        self.Score = sc
        self.TimeBonus = tb

        self.root.mainloop()


# Function to generate new leaderboard object

def NewLeaderBoard(nm):

    global root

    establishConnection(nm)

    root = tk.Tk(className = " Leader Board ")
    root.resizable(0,0)
    obj = LeaderBoard(master = root)
    root.protocol("WM_DELETE_WINDOW",root.destroy)

    return obj
