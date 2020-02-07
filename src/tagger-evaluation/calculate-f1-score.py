#!/usr/bin/env python3
from __future__ import division
"""
Implementation of F1 score

Calculating F1 score to compare the manual annotations.
Also comparing efficiency of different algorithms against manual annotations.

"""
from collections import Counter
from pathlib import Path
import pandas as pd


def Convert(string):
    """

    :param string: Input string
    :return: list from the string
    """
    li = list(string.split(","))
    print(li)
    return li


def combine_lists(list1,list2):

    """
    :param list1: 1st list
        first list with unique values
    :param list2: 2nd list
        second list with unique values
    :return: list
    """
    common = sorted(list((Counter(list1) & Counter(list2)).elements()))

    list1_updated = list((Counter(list1) - Counter(common)).elements())
    list2_updated = list((Counter(list2) - Counter(common)).elements())

    final_list = sorted(list1_updated + list2_updated + common)

    return final_list


def change_list_size(bigger_list,smaller_list):
    """

    :param bigger_list: Big / Combined list
    :param smaller_list: list which is converted to the size of bigger list
    :return: converted smaller list
    """
    converted_list = []
    for x in bigger_list:
        if x in smaller_list:
            converted_list.append(x)
            smaller_list.remove(x)
        else:
            converted_list.append(None)
    #print(converted_list)
    return converted_list


def compare_calculate_f1_score(converted_list1,convrted_list2):

    """

    :param converted_list1: List 1 to be compared
    :param convrted_list2: List 2 to be compared
    :return: F1 score
    """

    true_positive_list = [i == j for i, j in zip(converted_list1, convrted_list2)]
    true_positive = len([x for x in true_positive_list if x is True])
    print("true positive = " + str(true_positive))

    false_positive = len([x for x in converted_list1 if x is None])
    print("false positive = " + str(false_positive))

    false_negative = len([x for x in convrted_list2 if x is None])
    print("false negative = " + str(false_negative))

    precision = true_positive / (true_positive + false_positive)
    recall = true_positive / (true_positive + false_negative)
    F1 = 2 * ((precision * recall) / (precision + recall))

    print("precision = " + str(precision))
    print("recall = " + str(recall))
    print("F1 score = " + str(F1))

    with open(datapath / 'data/hugh-murray/chapter3/chapter3-results-combined.txt', 'a') as f:
<<<<<<< HEAD
        f.write("\n ======================== allenNLP Person with index ========================")
=======
        f.write("\n ======================== Gazzeter Location ========================")
>>>>>>> d24deadf2a6f9fed869dd7c203e797b8cf0fb398
        f.write("\n")
        f.write("\ntrue positive = %s" % str(true_positive))
        f.write("\nfalse positive = %s" % str(false_positive))
        f.write("\nfalse negative = %s" % str(false_negative))
        f.write("\nprecision = %s" % str(precision))
        f.write("\nrecall = %s" % str(recall))
        f.write("\nF1 score = %s" % str(F1))
        f.write("\n")
        return F1


datapath = Path(__file__).resolve().parents[2]
<<<<<<< HEAD
readfile = datapath / 'data/hugh-murray/chapter3/chapter3-gazetter-allenNLP.csv' # Input individual index files

data = pd.read_csv(readfile,sep='\t', encoding='latin1',error_bad_lines=False)
str1 = data['Gazzeter Person'].str.cat(sep=',')
str2 = data['allenNLP Person'].str.cat(sep=',')
=======
readfile = datapath / 'data/hugh-murray/chapter3/chapter3-gazetter-combined.csv' # Input individual index files

data = pd.read_csv(readfile,sep=',', encoding='latin1',error_bad_lines=False)
str1 = data['Location'].str.cat(sep=',')
str2 = data['Gazzeter Location'].str.cat(sep=',')
>>>>>>> d24deadf2a6f9fed869dd7c203e797b8cf0fb398

#str1 = "Kublai,Khan,Chengiz,Chengiz,Khan"
#str2 = "Khan,Nayan,Nayan,Achmac,Kublai,Nayan"

print("========== Two lists to compare==========")
print(str1)
print(str2)
print(" ")

list_of_str1 = sorted(Convert(str1))
list_of_str2 = sorted(Convert(str2))

cleaned_list_of_str1 = [item.strip() for item in list_of_str1]
cleaned_list_of_str2 = [item.strip() for item in list_of_str2]

print("========== Calculation of precision, recall and F1 ==========")


combined_list = combine_lists(cleaned_list_of_str1, cleaned_list_of_str2)
print(combined_list)
print(" ")
print("================================")

converted_list1 = change_list_size(combined_list,cleaned_list_of_str1)
converted_list2 = change_list_size(combined_list,cleaned_list_of_str2)

print(converted_list1)
print(converted_list2)
F1 = compare_calculate_f1_score(converted_list1,converted_list2)