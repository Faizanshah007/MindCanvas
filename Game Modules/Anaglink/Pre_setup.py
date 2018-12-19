from itertools import permutations
import enchant
import csv
import os, sys

loaded = 0

anaglist = list()

def prepare():

    # Preparing Data

    d = enchant.Dict("en_US")

    def meaningful(string):
        return d.check(string)

    def jumbleword(wrd):
            
        testset = set([''.join(p) for p in permutations(wrd)])
        anag = []
        for case in testset:
            if meaningful(case):
                anag.append(case)
        return anag

    list1=[]
    list2=[]
    list3=[]

    # Appending words into their respected lists

    with open('4-word.csv', 'r') as csvfile:
        rd = csv.reader(csvfile)
        for row in rd:
            list1.append(row[0])
    csvfile.close()

    with open('5-word.csv', 'r') as csvfile:
        rd = csv.reader(csvfile)
        for row in rd:
            list2.append(row[0])
    csvfile.close()

    with open('7-word.csv', 'r') as csvfile:
        rd = csv.reader(csvfile)
        for row in rd:
            list3.append(row[0])
    csvfile.close()


    # Generating and storing all possible anagrams into anaglist

    global loaded, anaglist

    inc3 = 108/len(list3)

    for w in list3:

        loaded = loaded + inc3
        
        anaglist.append(jumbleword(w))

    inc2 = 9.6/len(list2)

    for w in list2:

        loaded = loaded + inc2
        
        anaglist.append(jumbleword(w))

    inc1 = 2.4/len(list1)

    for w in list1:

        loaded = loaded + inc1
        
        anaglist.append(jumbleword(w))


# Converting into set and returning for better mobility

def get():
    st = set()
    for anag in anaglist:
        st.add(tuple(anag))
    return st



