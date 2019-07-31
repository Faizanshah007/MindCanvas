import math
import Core


#  Scoring Scheme :
#  2 word link = 3 * ( 1 + 0.9 ) score increment
#  3 word link = 3 * ( 1 + 0.9 + 0.8 ) score increment
#  n word link = 3 * ( 1 + 0.9 + 0.8 + ... + ( 1 + ( n - 1 ) * (-0.1) ) ) score increment

def update_score(score, val, stat):

    # In this case val = length of the link
    if( stat != 'Won' and stat != 'Lost' ):
        increment = 3 * ((val / 2) * (2 + (val - 1) * (-0.1)))  # Sum up to n terms of an A.P.
        return(math.ceil(score + increment))

    # In this case val = Time remaining
    elif( stat == 'Won' ):
        increment = math.floor(val * 0.5)
        Core.TimeBonus = increment
        return(score + increment)
