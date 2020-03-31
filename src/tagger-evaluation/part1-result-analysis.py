import pandas as pd
import numpy as np
from pathlib import Path
from collections import Counter

def Convert(string):
    """

    :param string: Input string
    :return: list from the string
    """
    if not isinstance(string,float):
        li = list(string.split(","))
        print(li)
    else:
        li = []
    return li

datapath = Path(__file__).resolve().parents[2]

readfile = datapath / 'data/hugh-murray/part1/chapter1-gazetter-allenNLP.csv' # Input individual index files

data = pd.read_csv(readfile,sep='\t', encoding='latin1',error_bad_lines=False)

not_gazetter = []
count = 0

for index,row in data.iterrows():

    person_gazetter = row['Gazzeter Person']
    person = row['Person']

    person_gazetter_list = sorted(Convert(person_gazetter))
    person_list = sorted(Convert(person))

    person_gazetter_cleaned_list = [item.strip() for item in person_gazetter_list]
    person_cleaned_list = [item.strip() for item in person_list]

    common = sorted(list((Counter(person_gazetter_cleaned_list) & Counter(person_cleaned_list)).elements()))

    not_in_gazetter_list = list((Counter(person_cleaned_list) - Counter(common)).elements())

    not_in_gazetter = ', '.join([str(elem) for elem in not_in_gazetter_list])
    not_gazetter.append(not_in_gazetter)
    count = count + 1
    print(count)

data['Not Gazetter'] = not_gazetter

writefile = datapath / 'data/hugh-murray/part1/chapter1-notgazetter-allenNLP.csv' # Input individual index files

data.to_csv(writefile, sep='\t', encoding='latin1')


