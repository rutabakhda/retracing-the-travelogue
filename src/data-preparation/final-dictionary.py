import os
from pathlib import Path
import pandas as pd

datapath = Path(__file__).resolve().parents[2]

print(f'Current working directory: {datapath}')

"""
    This code combines 2 different versions of indexes.
    
    There two different indexes as csv from two authors : Murray and Yule.
    Each entry(entity) is annotated in both indexes manually with 3 different 
    Tags : Location, Person, Organization.
    This code combines these 2 indexes along with their tags and generates final index.
     
"""


def combine_lists(list1, list2):

    """
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
    return [final_list,common_words,unique_in_list1]


def list_to_csv(list, dataframe1, dataframe2,common_words,unique_in_murray):

    """
    :param list: list that needs to be stored as csv
    :param dataframe1: dataframe of 1st index
    :param dataframe2: dataframe of 2nd index
    :return:
    """

    new_data = pd.DataFrame(columns=['Entity', 'Tag'])
    new_row = {}
    for entry in list:

        if entry in common_words:
            reference = 'Murray,Yule'
        elif entry in unique_in_murray:
            reference = 'Murray'
        else:
            reference = 'Yule'

        temp1 = dataframe1[dataframe1['Entity Name'] == entry]
        temp2 = dataframe2[dataframe2['Entity Name'] == entry]
        if not temp1.empty:
            tag = temp1['Tag'].iloc[0]
        elif not temp2.empty:
            tag = temp2['Tag'].iloc[0]
        else:
            tag = " "
        new_row["Entity"] = entry
        new_row['Tag'] = tag
        new_row['Reference'] = reference
        new_data.loc[len(new_data)] = new_row
    new_data.to_csv(datapath + "final-list.csv", sep=',', encoding='latin1')


readfile_murray = datapath / 'data/hugh-murray/index/index.csv'
readfile_yule = datapath / 'data/henry-yule/index/Book1.txt'

# Reads csv of index and convert it into list with unique entities
df_murray=pd.read_csv(readfile_murray,sep=',',encoding='latin1')
murray_list = df_murray['Entity Name'].unique().tolist()

df_yule=pd.read_csv(readfile_yule,sep='\t',encoding='latin1')
yule_list = df_yule['Entity Name'].unique().tolist()

final_list,common_words,unique_in_murray = combine_lists(murray_list,yule_list)

list_to_csv(final_list,df_murray,df_yule,common_words,unique_in_murray)
