import os
import pandas as pd

basepath = os.path.dirname(os.path.abspath(__file__))
datapath = basepath + '/data/'

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
    return final_list


def list_to_csv(list, dataframe1, dataframe2):

    """
    :param list: list that needs to be stored as csv
    :param dataframe1: dataframe of 1st index
    :param dataframe2: dataframe of 2nd index
    :return:
    """

    new_data = pd.DataFrame(columns=['Entity', 'Tag'])
    new_row = {}
    for entry in list:
        temp = dataframe1[dataframe1['Entity Name'] == entry]
        if temp.empty:
            tag = " "
        else:
            tag = temp['Tag'].iloc[0]
        new_row["Entity"] = entry
        new_row['Tag'] = tag
        new_data.loc[len(new_data)] = new_row
    new_data.to_csv(datapath + "final-list.csv", sep=',', encoding='latin1')


readfile_murray = 'hugh-murray/index/index.csv'
readfile_yule = 'henry-yule/index/Book1.txt'

# Reads csv of index and convert it into list with unique entities
df_murray=pd.read_csv(datapath+readfile_murray,sep=',',encoding='latin1')
murray_list = df_murray['Entity Name'].unique().tolist()

df_yule=pd.read_csv(datapath+readfile_yule,sep='\t',encoding='latin1')
yule_list = df_yule['Entity Name'].unique().tolist()

final_list = combine_lists(murray_list,yule_list)
list_to_csv(final_list,df_murray,df_yule)

