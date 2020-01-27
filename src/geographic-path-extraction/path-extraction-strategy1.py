#!/usr/bin/env python3
import pandas as pd
from pathlib import Path
from collections import Counter

datapath = Path(__file__).resolve().parents[2]
# Input individual index files
readfile = datapath / 'data/hugh-murray/chapter1/chapter1.csv'

data = pd.read_csv(readfile,sep=',', encoding='latin1',error_bad_lines=False)

section_data = data.groupby('sectionNo')


def convert_to_list(str):
    return str.split(",")

count = 0

for section in section_data:
    for item in section:
        if isinstance(item,pd.DataFrame):
            loc = item['Location'].dropna()
            location_list = loc.astype(str).apply(lambda s:convert_to_list(s))
            location = []

            for item in location_list:
                location = location + item
            count = count + 1

            item_count = dict(Counter(location))
            print(count)
            print(type(item_count))
            print(item_count)

    with open(datapath / 'data/hugh-murray/chapter1/chapter1-location-count.txt', 'a') as f:
         f.write("\n")
         f.write("\n ======================== Section %s ========================" % str(count))
         f.write("\n%s" % str(item_count))
         f.write("\n")
