------------------------------
Memorability Scores
------------------------------
Updated December 17, 2013

The 10k US Adult Faces Database was used in a study looking at consistency of memorability scores across a population. The set was split into 2,222 target photos, 6,468 filler photos, 30 demo photos, and 1,280 photos not used in the experiment.

For each target photo, we have memorability scores (misses, hits, correct rejections, false alarms) from approximately 80 subjects. These were collected from a large-scale crowdsourcing study on Amazon Mechanical Turk, where subjects saw a stream of face photographs and indicated when they saw a photograph repeat. Target photos repeated approximately every 91-109 images. We find that memorability (both hit rate and false alarm rate) are indeed consistent across a population. Please refer to the paper for specific details on the methodology and results.
 
**Be sure to cite this paper when using anything from this dataset:**

Bainbridge, W. A., Isola, P., & Oliva, A. (2013). The Intrinsic Memorability of Face Photographs. Journal of Experimental Psychology: General, 142(4), 1323 - 1334.
------------------------------
Contents:

license-agreement.txt
The license agreement attached to this database. You must agree to the terms of this license agreement to use this database.

target-filenames.txt
For this experiment, attributes and labels were collected for 2,222 target photos in a memory game. The target file names from the original database were renamed to number labels (1-2222) for ease of use. This is a text file indicating the number label for each of the 2,222 target images. These number labels are particularly useful for accessing the data in the MATLAB structures.

memorability-scores.mat
A MATLAB structure containing memorability scores for the 2,222 target images. These memorability scores are coded as matrices, and the memorability score for a specific image can be accessed with its image number label (#1-2222 as coded in target-filenames.txt). The scores include hits, misses, false alarms, correct rejections, hit rate (HR), and false alarm rate (FAR). Hit rate is calculated as HR = HITS / (HITS + MISSES), while false alarm rate is calculated as FAR = FALSE ALARMS / (FALSE ALARMS + CORRECT REJECTIONS). An average of 80 hit rate scores were collected per image (with some variability due to the random presentation of images in the memory game, and participants ending the game at various times).

memorability-scores.xlsx
An Excel spreadsheet with memorability scores for the 2,222 target images (images #1-2222 as coded in target-filenames.txt). The scores include hits, misses, false alarms, correct rejections, hit rate (HR), and false alarm rate (FAR). Hit rate can be calculated as HR = HITS / (HITS + MISSES), while false alarm rate can be calculated as FAR = FALSE ALARMS / (FALSE ALARMS + CORRECT REJECTIONS). An average of 80 hit rate scores were collected per image (with some variability due to the random presentation of images in the memory game, and participants ending the game at various times).

subject-demographics.xlsx
An Excel spreadsheet with demographics and information for each of the 1025 participants in this experiment (note: not all participants made it past the demo of the study). The following is a description of each column:
- Column A : Did the participant pass the demo and move onto the real experiment or not?
- Column B : The participant's age
- Column C : How many target photos the participant saw
- Column D : The furthest level reached by the participant (up to 30)
- Column E : Participant's race. The participant could choose to indicate no race (null values), and also to mark multiple races. Race options were chosen based on common racial demographics on Amazon Mechanical Turk. The numbers correspond to:
	0 = White
	1 = Black
	2 = East Asian
	3 = South Asian
	4 = Hispanic
	5 = Middle Eastern
	6 = Other
	7 = Prefer not to say
- Column F : Participant's gender.
	0 = Male
	1 = Female
	2 = Prefer not to say
- Column G : Date of the subject's participation
- Column H : A counter for how often the subject failed the vigilance task
- Column I : Number of filler images seen by the subject