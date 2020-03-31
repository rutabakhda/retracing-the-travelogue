#!/usr/bin/env python3
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
from nltk import Tree
from nltk.tag import StanfordPOSTagger
from pathlib import Path
import pandas as pd
import os

def get_continuous_chunks(text, label):

    #tagged_text = tagger.tag(text.split())
    #nouns = [word for word,tag in tagged_text if tag.startswith('NN')]
    #print(nouns)

    tokenized_text = word_tokenize(text)
    classified_text = st.tag(tokenized_text)

    tags = [word for word,tag in classified_text if tag == label]
    return tags


sentence = 'for it is the custom of the Tartars, that until the horn termed naccar is winded the troops do not engage.'

datapath = Path(__file__).resolve().parents[2]


stanford_dir = datapath / 'tools/standford-nlp/stanford-postagger-2018-10-16'
model_file = stanford_dir / 'models/english-bidirectional-distsim.tagger'
jar_file = stanford_dir / 'stanford-postagger.jar'

st = StanfordNERTagger('../../tools/standford-nlp/stanford-ner-2018-10-16/classifiers/english.all.3class.distsim.crf.ser.gz',
                       '../../tools/standford-nlp/stanford-ner-2018-10-16/stanford-ner.jar', encoding='utf-8')

tagger = StanfordPOSTagger(model_filename=str(model_file), path_to_jar=str(jar_file))

# Input individual index files
#readfile = datapath / 'data/hugh-murray/chapter1/chapter1.csv'
#data = pd.read_csv(readfile,sep=',', encoding='latin1',error_bad_lines=False)

def tagger_stanford(data):
    location_list = []
    person_list = []
    organization_list = []

    count = 0
    for index,row in data.iterrows():
        sentence = row['sentence']
        ner_location = get_continuous_chunks(sentence, 'LOCATION')
        ner_person = get_continuous_chunks(sentence, 'PERSON')
        ner_organization = get_continuous_chunks(sentence, 'ORGANIZATION')

        location = ','.join([str(elem) for elem in ner_location])
        person = ','.join([str(elem) for elem in ner_person])
        organization = ','.join([str(elem) for elem in ner_organization])

        location_list.append(location)
        person_list.append(person)
        organization_list.append(organization)
        count = count + 1
        print(count)


    data['Standford Location'] = location_list
    data['Standford Person'] = person_list
    data['Stadnford Organization'] = organization_list
    return data

#book = ['part1','part2','part3']
book = ['part2','part3']

for part in book:

    readfile = datapath / 'results/hugh-murray/{}/processed/{}-annotated-special.csv'.format(part,part)
    data = pd.read_csv(readfile, sep='\t', encoding='latin1', error_bad_lines=False)

    outdata = tagger_stanford(data)

    if not os.path.exists(str(datapath) + '/results/hugh-murray/{}/ner'.format(part)):
       os.makedirs(str(datapath) + '/results/hugh-murray/{}/ner'.format(part))

    writefile = str(datapath) + '/results/hugh-murray/{}/ner/stanford.csv'.format(part)
    if os.path.exists(writefile):
        os.remove(writefile)

    outdata.to_csv(writefile, sep='\t', encoding='latin1',index=False)

