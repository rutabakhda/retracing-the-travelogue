#!/usr/bin/env python3
from collections import Counter
from pathlib import Path
import pandas as pd
import  os

def Convert(string):
    """

    :param string: Input string
    :return: list from the string
    """
    li = list(string.split(","))
    return li


datapath = Path(__file__).resolve().parents[2]

def verb_voting(data):
    verb_list = []
    count = 0
    for index,row in data.iterrows():
        str1 = row['WordNet Travel']
        str2 = row['VerbNet Travel']
        str3 = row['FrameNet Travel']


        if pd.isnull(str1):
            list_of_str1 = []
        else:
            list_of_str1 = sorted(Convert(str1))

        if pd.isnull(str2):
            list_of_str2 = []
        else:
            list_of_str2 = sorted(Convert(str2))

        if pd.isnull(str3):
            list_of_str3 = []
        else:
            list_of_str3 = sorted(Convert(str3))

        common1 = sorted(list((Counter(list_of_str1) & Counter(list_of_str2)).elements()))
        common2 = sorted(list((Counter(list_of_str2) & Counter(list_of_str3)).elements()))
        common3 = sorted(list((Counter(list_of_str3) & Counter(list_of_str1)).elements()))
        common_in_all = sorted(set(common1) & set(common2) & set(common3))

        common1_updated = list((Counter(common1) - Counter(common_in_all)).elements())
        common2_updated = list((Counter(common2) - Counter(common_in_all)).elements())
        common3_updated = list((Counter(common3) - Counter(common_in_all)).elements())

        final = sorted(common1_updated + common2_updated + common3_updated + common_in_all)

        verbs = ' ,'.join([str(elem) for elem in final])
        verb_list.append(verbs)

        count = count + 1
        print(count)

    data['Voted Travel'] = verb_list

    return data


book = ['part1']

for part in book:

    readfile = datapath / 'results/hugh-murray/{}/geograhpic-path-extraction/{}-annotated-with-verbs.csv'.format(part,part)
    data = pd.read_csv(readfile, sep='\t', encoding='latin1', error_bad_lines=False)

    outdata = verb_voting(data)

    writefile = datapath / 'results/hugh-murray/{}/geograhpic-path-extraction/{}-annotated-with-verbs.csv'.format(part,part)
    if os.path.exists(writefile):
        os.remove(writefile)

    outdata.to_csv(writefile, sep='\t', encoding='latin1',index=False)