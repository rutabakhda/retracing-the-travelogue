#!/usr/bin/venv python3
"""
    This code combines 2 different versions of indexes.

    There two different indexes as csv from two authors : Murray and Yule.
    Each entry(entity) is annotated in both indexes manually with 3 different
    tags : Location, Person, Organization.
    This code combines these 2 indexes along with their tags and generates one final tagged index.

"""

import pandas as pd
from pathlib import Path
import os

def combine_lists(list1, list2):
    """
    This function combines two lists by removing duplicates and keeping only unique values.
    :param list1: 1st list
        first list with unique values
    :param list2: 2nd list
        second list with unique values
    :return: list
    """
    common_words = list(set(list2).intersection(list1))

    unique_in_list1 = [x for x in list1 if x not in common_words]

    final_list = (unique_in_list1 + list2)
    final_list = sorted(final_list)
    return [final_list, common_words, unique_in_list1]


def list_to_csv(list, dataframe1, dataframe2, common_words, unique_in_murray):
    """
    Converts combined list to csv along with tag and book reference.
    :param common_words: Commond words in both lists of index
    :param unique_in_murray: words unique in murray index
    :param list: final list(combined index list) that needs to be stored as csv
    :param dataframe1: datafrme of 1st index
    :param dataframe2: dataframe of 2nd index
    :return:
    """

    new_data = pd.DataFrame(columns=['Entity Name', 'Alternative Name', 'Tag', 'Reference'])
    new_row = {}
    for entry in list:
        # Assigning book reference
        if entry in common_words:
            reference = 'Murray,Yule'
        elif entry in unique_in_murray:
            reference = 'Murray'
        else:
            reference = 'Yule'

        # Finding whole record with tag from individual book index
        #entry_str = entry.encode('utf8')  # Converts from unicode to string for comparision
        temp1 = dataframe1.loc[dataframe1['Entity Name'] == entry]  # checks if an entry belongs to murray index
        temp2 = dataframe2[dataframe2['Entity Name'] == entry]  # checks an entry belongs to yule index
        alternative_name = []

        # Fetching tag
        if not temp1.empty:

            tag = temp1['Tag'].iloc[0]
            alternative_name.append(temp1['Alternative Name'].iloc[0])
        elif not temp2.empty:

            tag = temp2['Tag'].iloc[0]
            alternative_name.append(temp2['Alternative Name'].iloc[0])
        else:

            tag = " " # tags are not assigned to irrelevant data

        alternative_name_cleaned = [x for x in alternative_name if str(x) != 'nan']
        
        if not isinstance(alternative_name_cleaned,float):

            alternative = ','.join(alternative_name_cleaned)
        else:

            alternative = " "

        new_row["Entity Name"] = entry
        new_row["Alternative Name"] = alternative
        new_row['Tag'] = tag
        new_row['Reference'] = reference
        new_data.loc[len(new_data)] = new_row

    if not os.path.exists(datapath / 'results/murray-yule/index'):
        os.makedirs(datapath / 'results/murray-yule/index')

    new_data.to_csv(datapath / "results/murray-yule/index/murray-yule-index.csv", sep='\t', encoding='utf-8-sig')


datapath = Path(__file__).resolve().parents[2]

# Input individual index files
readfile_murray = datapath / 'results/hugh-murray/index/processed/index-annotated.csv'
readfile_yule = datapath / 'results/henry-yule/index/processed/index-corrected.csv'

# Reads csv of index and convert it into list with unique entities
df_murray = pd.read_csv(readfile_murray, sep=',', encoding='utf-8-sig')
murray_list = df_murray['Entity Name'].unique().tolist()
df_yule = pd.read_csv(readfile_yule, sep='\t', encoding='utf-8-sig')
yule_list = df_yule['Entity Name'].unique().tolist()

# Combining lists with unique values
final_list, common_words, unique_in_murray = combine_lists(murray_list, yule_list)
print(final_list)
# Saving combined list with tags and book reference as csv
list_to_csv(final_list, df_murray, df_yule, common_words, unique_in_murray)

print("completed")
