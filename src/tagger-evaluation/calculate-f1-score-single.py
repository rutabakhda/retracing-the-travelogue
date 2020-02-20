#!/usr/bin/env python3
from __future__ import division
from collections import Counter
import os
import pandas as pd
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


def compare_calculate_f1_score(converted_list1,convrted_list2,part,entity):

    """

    :param converted_list1: List 1 to be compared
    :param convrted_list2: List 2 to be compared
    :return: F1 score
    """

    true_positive_list = [i == j for i, j in zip(converted_list1, convrted_list2)]
    true_positive = len([x for x in true_positive_list if x is True])
    print("true positive = " + str(true_positive))

    false_positive_list = [x for x in converted_list1 if x is None]
    false_positive = len([x for x in converted_list1 if x is None])
    print("false positive = " + str(false_positive))

    false_negative_list = [x for x in convrted_list2 if x is None]
    false_negative = len([x for x in convrted_list2 if x is None])
    print("false negative = " + str(false_negative))

    precision = true_positive / (true_positive + false_positive)
    recall = true_positive / (true_positive + false_negative)
    F1 = 2 * ((precision * recall) / (precision + recall))

    print("precision = " + str(precision))
    print("recall = " + str(recall))
    print("F1 score = " + str(F1))

    counter1 = Counter(converted_list1)
    counter2 = Counter(converted_list2)

    if not os.path.exists(datapath / 'results/hugh-murray/{}/ner/result-analysis'.format(part)):
       os.makedirs(datapath / 'results/hugh-murray/{}/ner/result-analysis'.format(part))

    with open(datapath / 'results/hugh-murray/{}/ner/result-analysis/allenNLP.txt'.format(part), 'a') as f:
        f.write("\n ======================== %s ========================" % str(entity))
        #for i in range(1, len(converted_list1)):
        #  f.write("\n%s" % str(converted_list1[i]))
        #  f.write("\n%s" % str(converted_list2[i]))
        f.write("\n precision = %s " % str(precision))
        f.write("\n recall = %s" % str(recall))
        f.write("\n F1 score = %s" % str(F1))
        f.write("\n")
        f.write("\n")
        f.write("\n true positive = %s " % str(true_positive))
        f.write("\n false positive = %s" % str(false_positive))
        f.write("\n false negative = %s" % str(false_negative))
        f.write("\n")
        f.write("\n")
        f.write("\n")
        f.write("\n%s" % str(counter1))
        f.write("\n")
        f.write("\n")
        f.write("\n%s" % str(counter2))


    print("******************************************************")
    print(type(counter1))
    counter1_dict = dict(counter1)
    counter2_dict = dict(counter2)
    print(type(counter2_dict))
    entity_list = []
    original_count = []
    found_count = []
    for key in counter1_dict:
        print(key)
        print(counter1[key])
        print(counter2[key])
        print("===================")
        entity_list.append(key)
        original_count.append(counter1[key])
        found_count.append(counter2[key])

    df = pd.DataFrame(data={"Entity": entity_list, "Original count": original_count, "Found count": found_count})
    df.to_csv(datapath / 'results/hugh-murray/{}/ner/result-analysis/{}-allenNLP.csv'.format(part,entity), sep='\t', index=False)

datapath = Path(__file__).resolve().parents[2]

#book = ['part1','part2','part3']
book = ['part3']
tagger = "allenNLP"
entities = ['Location','Person']
#book = ['part1']

for part in book:

    readfile = datapath / 'results/hugh-murray/{}/ner/allenNLP.csv'.format(part) # Input individual index files

    data = pd.read_csv(readfile,sep='\t', encoding='latin1',error_bad_lines=False)

    for entity in entities:
        str1 = data[entity].str.cat(sep=',')
        str2 = data[tagger + " " + entity].str.cat(sep=',')

        list_of_str1 = sorted(Convert(str1))
        list_of_str2 = sorted(Convert(str2))

        cleaned_list_of_str1 = [item.strip() for item in list_of_str1]
        cleaned_list_of_str2 = [item.strip() for item in list_of_str2]

        combined_list = combine_lists(cleaned_list_of_str1, cleaned_list_of_str2)

        converted_list1 = change_list_size(combined_list,cleaned_list_of_str1)
        converted_list2 = change_list_size(combined_list,cleaned_list_of_str2)

        F1 = compare_calculate_f1_score(converted_list1,converted_list2,part,entity)