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


def generate_ngrams(tokens, n):
    # Use the zip function to help us generate n-grams
    # Concatentate the tokens into ngrams and return
    ngrams = zip(*[tokens[i:] for i in range(n)])
    return [" ".join(ngram) for ngram in ngrams]

def find_tag(df,series,common,series_type):
    ner_person = []
    ner_location = []

    if common:

        for entry in common:
            #print(entry)
            if series_type == "alternative":
                temp1 = df.loc[series.str.contains(entry, na=False)]
            elif series_type == "main":
                temp1 = df.loc[series.isin([entry])]
            #print(temp1)
            tag = temp1['Tag'].iloc[0]
            if tag == 'Person':
                ner_person.append(entry)

            elif tag == 'Location':
              ner_location.append(entry)
    return ner_person,ner_location



datapath = Path(__file__).resolve().parents[2]

# Input individual index files
readfile_murray = datapath / 'data/final-list.txt.csv'
df_murray = pd.read_csv(readfile_murray, sep=',', encoding='latin1')
df_murray['Entity Name'] = df_murray['Entity Name'].apply(lambda s: s.strip())
murray_list = df_murray['Entity Name'].unique().tolist()
murray_list = [item.strip() for item in murray_list]
#murray_list = [item.replace(".","") for item in murray_list]
murray_alternative_list = []

for index,item in df_murray['Alternative Name'].iteritems():
    if not isinstance(item,float):
        murray_alternative_list = murray_alternative_list + item.split(",")

murray_alternative_list = list(set(murray_alternative_list))#
murray_alternative_list = [value.strip() for value in murray_alternative_list]
#murray_alternative_list = [value.replace(".","") for value in murray_alternative_list]
readfile = datapath / 'data/hugh-murray/chapter3/chapter3-allenNLP.csv'
data = pd.read_csv(readfile,sep='\t', encoding='latin1',error_bad_lines=False)

location_list = []
person_list = []
count = 0


for index,row in data.iterrows():
    sentence = row['sentence']
    #sentence = ' and the dealers here convey the goods to various quarters in the west, whence the most valuable are forwarded to Alexandria.'
    sentence = sentence.replace(" and"," ")
    sentence = sentence.replace("The", "the")
    remove = string.punctuation
    remove = remove.replace("-", "")  # don't remove hyphens
    remove = remove.replace("'", "")  # don't remove hyphens
    pattern = r"[{}]".format(remove)
    sentence = re.sub(pattern," ",sentence)
    sentence_list = convert(sentence)
    sentence_list = [item.strip() for item in sentence_list]
    #print(sentence_list)
    sentence_bigram = generate_ngrams(sentence_list,2)
    sentence_trigram = generate_ngrams(sentence_list,3)
    #print(sentence_trigram)

    common_1gram = [value for value in sentence_list if value in murray_list]
    common_alternative_1gram = [value for value in sentence_list if value in murray_alternative_list]

    common_bigram = [value for value in sentence_bigram if value in murray_list]
    common_alternative_bigram = [value for value in sentence_bigram if value in murray_alternative_list]

    common_trigram = [value for value in sentence_trigram if value in murray_list]
    common_alternative_trigram = [value for value in sentence_trigram if value in murray_alternative_list]

    #print(common_1gram)
    #print(common_alternative_1gram)

    for value in (common_alternative_1gram + common_1gram):
        if any(value in s for s in (common_bigram + common_alternative_bigram)):
            if value in common_1gram:
                common_1gram.remove(value)
            if value in common_alternative_1gram:
                common_alternative_1gram.remove(value)

    for value in (common_alternative_1gram + common_1gram):
        if any(value in s for s in (common_trigram + common_alternative_trigram)):
            if value in common_1gram:
                common_1gram.remove(value)
            if value in common_alternative_1gram:
                common_alternative_1gram.remove(value)

    for value in (common_bigram + common_alternative_bigram):
        if any(value in s for s in (common_trigram + common_alternative_trigram)):
            if value in common_bigram:
                common_bigram.remove(value)
            if value in common_alternative_bigram:
                common_alternative_bigram.remove(value)


    ner_person = []
    ner_location = []

    [ner_person_main_1gram,ner_location_main_1gram] = find_tag(df_murray,df_murray['Entity Name'],common_1gram,"main")
    [ner_person_alternative_1gram,ner_location_alternative_1gram] = find_tag(df_murray,df_murray['Alternative Name'], common_alternative_1gram,"alternative")
    #print(ner_pepyrson_main_1gram)
    [ner_person_main_2gram,ner_location_main_2gram] = find_tag(df_murray,df_murray['Entity Name'],common_bigram,"main")
    [ner_person_alternative_2gram,ner_location_alternative_2gram] = find_tag(df_murray,df_murray['Alternative Name'], common_alternative_bigram,"alternative")

    [ner_person_main_3gram,ner_location_main_3gram] = find_tag(df_murray,df_murray['Entity Name'],common_trigram,"main")
    [ner_person_alternative_3gram,ner_location_alternative_3gram] = find_tag(df_murray,df_murray['Alternative Name'], common_alternative_trigram,"alternative")

    ner_person = ner_person_main_1gram + ner_person_main_2gram + ner_person_main_3gram + ner_person_alternative_1gram + ner_person_alternative_2gram + ner_person_alternative_3gram
    ner_location = ner_location_main_1gram + ner_location_main_2gram + ner_location_main_3gram + ner_location_alternative_1gram + ner_location_alternative_2gram + ner_location_alternative_3gram

    location = ', '.join([str(elem) for elem in ner_location])
    person = ' ,'.join([str(elem) for elem in ner_person])
    #print(location)
    location_list.append(location)
    person_list.append(person)
    count = count + 1
    print(count)

data['Gazzeter Location'] = location_list
data['Gazzeter Person'] = person_list

writefile = datapath / 'data/hugh-murray/chapter3/chapter3-gazetter-allenNLP.csv'

data.to_csv(writefile, sep='\t', encoding='latin1')
