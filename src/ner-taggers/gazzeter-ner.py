import pandas as pd
import string
from pathlib import Path
from collections import Counter
import re

def convert(string):
    """

    :param string: Input string
    :return: list from the string
    """
    li = list(string.split(" "))
    return li


datapath = Path(__file__).resolve().parents[2]

# Input individual index files
readfile_murray = datapath / 'data/hugh-murray/index/index.csv'
df_murray = pd.read_csv(readfile_murray, sep=',', encoding='latin1')
df_murray['Entity Name'] = df_murray['Entity Name'].apply(lambda s: s.strip())
murray_list = df_murray['Entity Name'].unique().tolist()

murray_list = [item.strip() for item in murray_list]

readfile = datapath / 'data/hugh-murray/chapter3/chapter3.csv'
data = pd.read_csv(readfile,sep=',', encoding='latin1',error_bad_lines=False)

location_list = []
person_list = []
count = 0


for index,row in data.iterrows():
    sentence = row['sentence']
    #sentence = "Having mentioned this King Dor, I will tell you a curious story of what passed between him and Prester John."
    remove = string.punctuation
    remove = remove.replace("-", "")  # don't remove hyphens
    remove = remove.replace("'", "")  # don't remove hyphens
    pattern = r"[{}]".format(remove)
    sentence = re.sub(pattern," ",sentence)
    #sentence = sentence.translate(str.maketrans(' ', ' ', string.punctuation))
    sentence_list = convert(sentence)
    print(sentence_list)
    #print(sentence_list)
    sentence_list = [item.strip() for item in sentence_list]
    common = [value for value in sentence_list if value in murray_list]
    print(common)
    ner_person = []
    ner_location = []
    for entry in common:
        print(entry)
        temp1 = df_murray.loc[df_murray['Entity Name'] == entry]
        tag = temp1['Tag'].iloc[0]
        print(tag)
        if tag == 'Person':
            ner_person.append(entry)

        elif tag == 'Location':
          ner_location.append(entry)

    location = ', '.join([str(elem) for elem in ner_location])
    person = ' ,'.join([str(elem) for elem in ner_person])

    location_list.append(location)
    person_list.append(person)
    count = count + 1
    print(count)

data['Gazzeter Location'] = location_list
data['Gazzeter Person'] = person_list

writefile = datapath / 'data/hugh-murray/chapter3/chapter3-gazzeter.csv'

data.to_csv(writefile, sep=',', encoding='latin1')
