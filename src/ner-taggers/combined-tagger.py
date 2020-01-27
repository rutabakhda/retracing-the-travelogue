<<<<<<< HEAD
#!/usr/bin/env python3
from collections import Counter
from pathlib import Path
import pandas as pd
import math

def Convert(string):
    """

    :param string: Input string
    :return: list from the string
    """
    li = list(string.split(","))
    return li


datapath = Path(__file__).resolve().parents[2]

# Input individual index files
readfile = datapath / 'data/hugh-murray/chapter1/chapter1-500-lines-annotated-final.csv'

data = pd.read_csv(readfile,sep='\t', encoding='latin1',error_bad_lines=False)

#person_nltk = data['NLTK Person']
#person_standford = data['Standford Person']
#person_spacy = data['spacy Person']

#location_nltk = data['NLTK Location']
#location_standford = data['Standford Location']
#location_spacy = data['spacy Location']

#str1 = 'Nayan,Kublai,Kaidu'
#str2 = 'Nayan,Nayan,Kublai,Ma'
#str3 = 'Kaidu,Baro,Nayan,Nayan'

person_list = []
count = 0
for index,row in data.iterrows():
    str1 = row['NLTK Location']
    str2 = row['Standford Location']
    str3 = row['Spacy Location']


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

    #list_of_str1 = sorted(Convert(str1))
    #list_of_str2 = sorted(Convert(str2))
    #list_of_str3 = sorted(Convert(str3))
    #print(list_of_str1)
    #print(list_of_str2)
    #print(list_of_str3)
    #print(" ")
    common1 = sorted(list((Counter(list_of_str1) & Counter(list_of_str2)).elements()))
    common2 = sorted(list((Counter(list_of_str2) & Counter(list_of_str3)).elements()))
    common3 = sorted(list((Counter(list_of_str3) & Counter(list_of_str1)).elements()))
    common_in_all = sorted(set(common1) & set(common2) & set(common3))
    #print(common1)
    #print(common2)
    #print(common3)
    #print(common_in_all)
    #print(" ")
    common1_updated = list((Counter(common1) - Counter(common_in_all)).elements())
    common2_updated = list((Counter(common2) - Counter(common_in_all)).elements())
    common3_updated = list((Counter(common3) - Counter(common_in_all)).elements())
    #print("updated = ")
    #print(common1_updated)
    #print(common2_updated)
    #print(common3_updated)
    #print("==========")
    final = sorted(common1_updated + common2_updated + common3_updated + common_in_all)
    #print(final)
    person = ' ,'.join([str(elem) for elem in final])
    person_list.append(person)

    count = count + 1
    print(count)

data['combined Location'] = person_list

writefile = datapath / 'data/hugh-murray/chapter1/chapter1-500-lines-annotated-final.csv'

data.to_csv(writefile, sep='\t', encoding='latin1')





=======
#!/usr/bin/env python3
from collections import Counter
from pathlib import Path
import pandas as pd

def Convert(string):
    """

    :param string: Input string
    :return: list from the string
    """
    li = list(string.split(","))
    return li




datapath = Path(__file__).resolve().parents[2]

# Input individual index files
readfile = datapath / 'data/hugh-murray/chapter1/chapter1-500-lines-annotated.csv'

data = pd.read_csv(readfile,sep='\t', encoding='latin1',error_bad_lines=False,nrows=5)

person_nltk = data['NLTK Person']
#person_standford = data['Standford Person']
person_spacy = data['spacy Person']

location_nltk = data['NLTK Location']
#location_standford = data['Standford Location']
location_spacy = data['spacy Location']

#for index,row in data.iterrows():

str1 = 'Nayan,Kublai,Kaidu'
str2 = 'Nayan,Nayan,Kublai,Ma'
str3 = 'Kaidu,Baro,Nayan,Nayan'

list_of_str1 = sorted(Convert(str1))
list_of_str2 = sorted(Convert(str2))
list_of_str3 = sorted(Convert(str3))
#print(list_of_str1)
#print(list_of_str2)
common1 = sorted(list((Counter(list_of_str1) & Counter(list_of_str2)).elements()))
print("common1 = ")
print(common1)

common2 = sorted(list((Counter(list_of_str2) & Counter(list_of_str3)).elements()))
print("common2 = ")
print(common2)

common3 = sorted(list((Counter(list_of_str3) & Counter(list_of_str1)).elements()))
print("common3 = ")
print(common3)
print("======================================================")
print("common all = ")
common_in_all = sorted(set(common1) & set(common2) & set(common3))
print(common_in_all)

common1_updated = list((Counter(common1) - Counter(common_in_all)).elements())
common2_updated = list((Counter(common2) - Counter(common_in_all)).elements())
common3_updated = list((Counter(common3) - Counter(common_in_all)).elements())

print("updated = ")
print(common1_updated)
print(common2_updated)
print(common3_updated)

final = sorted(common1_updated + common2_updated + common3_updated + common_in_all)
print("final=")
print(final)




>>>>>>> e35371d04a78bc1cc2c94a9efe0970e57a121f13
