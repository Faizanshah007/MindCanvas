import Pre_setup
import random
import csv

# Selecting 25 words from our anaglist (List of anagrams)

def produce():

    size = 0
    anag = Pre_setup.get()
    selec_list = []

    # Getting back anaglist from set
    anaglist = list(anag)

    while( size < 25 ):
        rnd = random.choice(anaglist)
        anaglist.remove(rnd)
        for r in rnd:
            if( size >= 25 ):
                break
            selec_list.append(r)
            size = size + 1
    random.shuffle(selec_list)

    return selec_list
