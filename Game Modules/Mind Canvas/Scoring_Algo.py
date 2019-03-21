from math import *
import Data

#Scoring Scheme :
#  2 word link = 3 * ( 1 + 0.9 ) score increment
#  3 word link = 3 * ( 1 + 0.9 + 0.8 ) score increment
#  n word link = 3 * ( 1 + 0.9 + 0.8 + ... + ( 1 + ( n - 1 ) * (-0.1) ) ) score increment

def update_score(s, l, stat):
    if( stat == 'None' ):
        increment = 3 * ((l / 2) * (2 + (l - 1) * (-0.1)))
        return(ceil(s + increment))
    elif( stat == 'Won' ):
        increment = floor((60 - l) * 0.5)
        Data.TimeBonus = increment
        return(s + increment)
