#!/usr/bin/venv python3
import pandas as pd
import string
from pathlib import Path
from collections import Counter
import re
import os

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


def get_gazetteer_data(readfile_murray):

    df_murray = pd.read_csv(readfile_murray, sep=',', encoding='latin1')
    df_murray['Entity Name'] = df_murray['Entity Name'].apply(lambda s: s.strip())

    murray_list = df_murray['Entity Name'].unique().tolist()
    murray_list = [item.strip() for item in murray_list]
    murray_alternative_list = []

    for index,item in df_murray['Alternative Name'].iteritems():
         if not isinstance(item,float):
             murray_alternative_list = murray_alternative_list + item.split(",")

    murray_alternative_list = list(set(murray_alternative_list))#
    murray_alternative_list = [value.strip() for value in murray_alternative_list]

    return [df_murray,murray_list,murray_alternative_list]


def preprocessing(sentence):
    remove = string.punctuation
    remove = remove.replace("-", "")  # don't remove hyphens
    remove = remove.replace("'", "")  # don't remove hyphens
    pattern = r"[{}]".format(remove)
    sentence = re.sub(pattern, " ", sentence)
    return sentence


def special_preprocessing(sentence):
    sentence = sentence.replace(" and", " ")
    sentence = sentence.replace("The", "the")
    sentence = sentence.replace(" khan","Khan")
    return sentence


def find_common_tokens(sentence_tokens, gazetteer_list):
    common = [value for value in sentence_tokens if value in gazetteer_list]
    return common

def find_entities(data,df_murray,murray_list,murray_alternative_list):
    location_list = []
    person_list = []
    count = 0


    for index,row in data.iterrows():
        sentence = row['sentence']

        sentence = preprocessing(sentence)
        sentence_onegram = convert(sentence)
        sentence_onegram = [item.strip() for item in sentence_onegram]

        sentence_bigram = generate_ngrams(sentence_onegram,2)
        sentence_trigram = generate_ngrams(sentence_onegram,3)

        common_onegram = find_common_tokens(sentence_onegram,murray_list)
        common_alternative_onegram = find_common_tokens(sentence_onegram,murray_alternative_list)

        common_bigram = find_common_tokens(sentence_bigram,murray_list)
        common_alternative_bigram =  find_common_tokens(sentence_bigram,murray_alternative_list)

        common_trigram = find_common_tokens(sentence_trigram,murray_list)
        common_alternative_trigram = find_common_tokens(sentence_trigram,murray_alternative_list)

        for value in (common_alternative_onegram + common_onegram):
            if any(value in s for s in (common_bigram + common_alternative_bigram)):
                if value in common_onegram:
                    common_onegram.remove(value)
                if value in common_alternative_onegram:
                    common_alternative_onegram.remove(value)

        for value in (common_alternative_onegram + common_onegram):
            if any(value in s for s in (common_trigram + common_alternative_trigram)):
                if value in common_onegram:
                    common_onegram.remove(value)
                if value in common_alternative_onegram:
                    common_alternative_onegram.remove(value)

        for value in (common_bigram + common_alternative_bigram):
            if any(value in s for s in (common_trigram + common_alternative_trigram)):
                if value in common_bigram:
                    common_bigram.remove(value)
                if value in common_alternative_bigram:
                    common_alternative_bigram.remove(value)

        [ner_person_main_1gram,ner_location_main_1gram] = find_tag(df_murray,df_murray['Entity Name'],common_onegram,"main")
        [ner_person_alternative_1gram,ner_location_alternative_1gram] = find_tag(df_murray,df_murray['Alternative Name'], common_alternative_onegram,"alternative")

        [ner_person_main_2gram,ner_location_main_2gram] = find_tag(df_murray,df_murray['Entity Name'],common_bigram,"main")
        [ner_person_alternative_2gram,ner_location_alternative_2gram] = find_tag(df_murray,df_murray['Alternative Name'], common_alternative_bigram,"alternative")

        [ner_person_main_3gram,ner_location_main_3gram] = find_tag(df_murray,df_murray['Entity Name'],common_trigram,"main")
        [ner_person_alternative_3gram,ner_location_alternative_3gram] = find_tag(df_murray,df_murray['Alternative Name'], common_alternative_trigram,"alternative")

        ner_person = ner_person_main_1gram + ner_person_main_2gram + ner_person_main_3gram + ner_person_alternative_1gram + ner_person_alternative_2gram + ner_person_alternative_3gram
        ner_location = ner_location_main_1gram + ner_location_main_2gram + ner_location_main_3gram + ner_location_alternative_1gram + ner_location_alternative_2gram + ner_location_alternative_3gram

        location = ', '.join([str(elem) for elem in ner_location])
        person = ' ,'.join([str(elem) for elem in ner_person])

        location_list.append(location)
        person_list.append(person)
        count = count + 1
        print(count)

    data['Gazzeter Location'] = location_list
    data['Gazzeter Person'] = person_list

    return data


datapath = Path(__file__).resolve().parents[2]
book = ['part1','part2','part3']

for part in book:

    readfile = datapath / 'results/hugh-murray/{}/processed/{}-annotated.csv'.format(part,part)
    data = pd.read_csv(readfile, sep='\t', encoding='latin1', error_bad_lines=False)

    readfile_murray = datapath / 'results/hugh-murray/index/processed/index-annotated.csv'
    df_murray,murray_list,murray_alternative_list = get_gazetteer_data(readfile_murray)

    outdata = find_entities(data,df_murray,murray_list,murray_alternative_list)

    if not os.path.exists(datapath / 'results/hugh-murray/{}/ner'.format(part)):
        os.makedirs(datapath / 'results/hugh-murray/{}/ner'.format(part))

    writefile = datapath / 'results/hugh-murray/{}/ner/gazetteer-murray-special-preprocessed.csv'.format(part)
    if os.path.exists(writefile):
        os.remove(writefile)

    outdata.to_csv(writefile, sep='\t', encoding='latin1')
