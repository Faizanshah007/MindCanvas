# This module is used during Game Task - 2
import string


selected_chr = ''


def anag_freq_alpha_selector(anaglinks, ignore_list):
    global selected_chr

    def freq_alpha_out(Input, mode = 0): # mode = 0 gives a list of selectable alphabets; mode = 1 gives frequent alphabets belonging to items in the ingnore_list
        count_dict = {alpha: 0 for alpha in string.ascii_uppercase}

        for anaglink in Input:
            for wrd in anaglink:
                for alpha in wrd:
                    count_dict[alpha.upper()] += 1

        result = sorted(count_dict.items(), reverse = bool(mode), key = lambda tup : tup[1]) # Sort the dict items according to their values in ascending/descending order according to the mode

        if(mode == 0):
            temp = list()
            for tup in result:
                if (tup[1] != 0):
                    temp.append(tup)
            result = temp

        return [tup[0] for tup in result]

    Ans_alpha = freq_alpha_out(anaglinks)
    nonAns_alpha = freq_alpha_out(ignore_list, 1)
    selected = ('', 51) # 51 = 50 (Maximum Possible Accumalative Index: 25 + 25) + 1

    for i in range(len(Ans_alpha)):
        accumalative_index = i + nonAns_alpha.index(Ans_alpha[i])
        if(accumalative_index < selected[1]):
            selected = (Ans_alpha[i], accumalative_index)

    selected_chr = selected[0]
    print(selected_chr.capitalize())
    return selected[0]


def run(anaglinks):
    global selected_chr

    for i in range(len(anaglinks)):
        if(selected_chr not in anaglinks[i][0].upper() and selected_chr != ''):
            anaglinks[i].append(-1) # Anaglinks without the selected character are invalid for the duration of the task
