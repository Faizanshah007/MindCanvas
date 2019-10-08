#MINDCANVAS

--------------------------------------------------------------------------------------------------------------------

Project Info.pdf : PDF deck containing project info.

--------------------------------------------------------------------------------------------------------------------

Project.mp4 : Demo Video

--------------------------------------------------------------------------------------------------------------------

MindCanvas 1.0 : Main game folder (Data Files & Source Code) -

  \- Expression Recognition  : Expression Recognition Module -
  
	~ [Source Code]      :
		label.py       : Uses CV2 to start cam capture.
		label_image.py : Uses previously generated graph to map the current expression captured by the cam.

  \- Game Modules            : Main modules used by the games -
  
	~ LeaderBoard    : A LeaderBoard library created by me.
	~ leaderboard.db : Stores the leaderboard data for the game.
	~ Result.txt     : Stores the clustering data that needs to be feeded into K-Means module.
	~ Summary.html   : Summary result of the previous game.
	~ 4-word.csv     : CSV containing 4 letter words.
	~ 5-word.csv     : CSV containing 5 letter words.
	~ 7-word.csv     : CSV containing 7 letter words.
	~ [Source Code]  :
		mc.py                : Root module of the game. It controls module initializations & Modifies system settings (Mouse speed, Sound, etc)
		Core.py              : Core of the game system. It acts as a interface between different modules.
		loading.py           : For calculating and displaying loading status.
		Leaderborad_Try.py   : For testing the LeaderBoard module.
		Pre_setup.py         : Takes in words from csv files and prepares them to be feeded into the anagram_generator.
		anagram_generator.py : Chooses the anagrams for the game.
		button.py            : Plots the buttons and controls their custom functionality.
		Scoring_Algo.py      : Caries out score calculations for the game.
		freq_alpha.py        : Selects an appropriate letter for task 2.
		rprint.py            : Thread safe version of print.

  \- Mouse Motion Analysis   : Analyzing player's mouse actions - 
  
	~ mousemodule.py [Source Code] : Manages players's DPI and Calculates players average speed.

  \- expression_output       : A file for "Message Passing" from Expression Module to Game Module.

  \- kmeans.py [Source Code] : K-Means clustering module.

  \- kmeans.txt              : Data for K-Means clustering.

--------------------------------------------------------------------------------------------------------------------

Zhao - Anxiety Inventory.pdf : One of the research papers referenced.

--------------------------------------------------------------------------------------------------------------------
