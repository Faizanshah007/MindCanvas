from cx_Freeze import setup, Executable
import os;

os.environ['TCL_LIBRARY'] = r'C:\Users\faiza\AppData\Local\Programs\Python\Python36\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\faiza\AppData\Local\Programs\Python\Python36\tcl\tk8.6'

setup(
    name ='ANAGRAM',
    version = "1.0" ,
    description = "Game Based on Anagrams" ,
    options = {"build_exe": {"packages":["pygame","time","math","os","itertools","enchant","random","csv","sqlite3","tkinter","PIL","win32api","threading","sys"],
                             "include_files":["Fonts","LeaderBoard","Media","anagram_generator.py","button.py","Data.py","loading.py","Pre_setup.py","Scoring_Algo.py"]}},
    executables = [Executable("anagram_game.pyw", base = "Win32GUI")],
    )
