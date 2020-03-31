#!/usr/bin/env python3

from pathlib import Path
import nltk
import string
from nltk import pos_tag,word_tokenize
from nltk.chunk import conlltags2tree, tree2conlltags
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk import Tree
import pandas as pd
import os

nltk.download('words')

# FACILITY, GPE, GSP, LOCATION, ORGANIZATION, PERSON
def get_continuous_chunks(sentence, label):
    tagged_text = ne_chunk(pos_tag(word_tokenize(sentence)))
    #print(tagged_text)
    #nouns = [word for word, tag in tagged_text if tag.startswith('NN')]
    #print(nouns)

    prev = None
    continuous_chunk = []
    current_chunk = []

    for subtree in tagged_text:
        if type(subtree) == Tree and subtree.label() == label:
            current_chunk.append(" ".join([token for token, pos in subtree.leaves()]))
        elif current_chunk:
            named_entity = " ".join(current_chunk)
            if named_entity not in continuous_chunk:
                continuous_chunk.append(named_entity)
                current_chunk = []
        else:
            continue

    return continuous_chunk


def convert_list_to_string(list):
    string1 = ','.join(map(str, list))
    return string1


datapath = Path(__file__).resolve().parents[2]

# Input individual index files
#readfile = datapath / 'data/hugh-murray/chapter2/chapter2.csv'

#data = pd.read_csv(readfile,sep=',', encoding='latin1',error_bad_lines=False)
#gpe_list = []

#data['sentence1'] = data['sentence'].apply(lambda s:get_continuous_chunks(s,'GPE'))
#data['sentence1'] = data['sentence1'].apply(lambda s:convert_list_to_string(s))
#string1 = data['sentence1'].str.cat(sep=',')
#li = list(string1.split(","))

#print(li)
#print("======================")
def tagger_nltk(data):
    count = 0
    location_list = []
    person_list = []
    organization_list = []

    for index,row in data.iterrows():
        sentence = row['sentence']
        #exclude = set(string.punctuation)
        #sentence = ''.join(ch for ch in sentence if ch not in exclude)
        ner_gpe = get_continuous_chunks(sentence, 'GPE')
        ner_location = get_continuous_chunks(sentence, 'LOCATION')
        ner_person = get_continuous_chunks(sentence, 'PERSON')
        ner_organization = get_continuous_chunks(sentence, 'ORGANIZATION')


        all_location = ner_location + ner_gpe

        #all_location = ner_gpe
        #gpe = ', '.join([str(elem) for elem in ner_gpe])
        location = ', '.join([str(elem) for elem in all_location])
        person = ' ,'.join([str(elem) for elem in ner_person])
        organization = ' ,'.join([str(elem) for elem in ner_organization])

        #gpe_list.append(gpe)
        location_list.append(location)
        person_list.append(person)
        organization_list.append(organization)
        count = count + 1
        print(count)

    data['NLTK Location'] = location_list
    #data['NLTK GPE'] = gpe_list
    data['NLTK Person'] = person_list
    data['NLTK organization'] = organization_list

    return data

book = ['part1','part2','part3']
#book = ['part1']

for part in book:

    readfile = datapath / 'results/hugh-murray/{}/processed/{}-annotated-special.csv'.format(part,part)
    data = pd.read_csv(readfile, sep='\t', encoding='latin1', error_bad_lines=False)

    outdata = tagger_nltk(data)

    if not os.path.exists(str(datapath) + '/results/hugh-murray/{}/ner'.format(part)):
       os.makedirs(str(datapath) + '/results/hugh-murray/{}/ner'.format(part))

    writefile = str(datapath) + '/results/hugh-murray/{}/ner/nltk.csv'.format(part)
    if os.path.exists(writefile):
        os.remove(writefile)

    outdata.to_csv(writefile, sep='\t', encoding='latin1',index=False)







