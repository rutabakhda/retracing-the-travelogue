#!/usr/bin/env python3
from __future__ import unicode_literals
import spacy
import pandas as pd
import string
from spacy import displacy
from pathlib import Path

#text = "There are also tablets whereon is sculptured a gerfalcon, which he gives to three great barons, who have then equal authority with himself."
#nlp = spacy.load("en")
#doc = nlp(text.decode('utf-8'))

datapath = Path(__file__).resolve().parents[2]

# Input individual index files
readfile = datapath / 'data/hugh-murray/chapter2/chapter2.csv'
#
# location_list = []
# person_list = []
# organization_list = []
#
data = pd.read_csv(readfile,sep=',', encoding='latin1',error_bad_lines=False)
location_list = []
person_list = []
org_list = []

count = 0
for index,row in data.iterrows():
     text = row['sentence']
     #exclude = set(string.punctuation)
     #text = ''.join(ch for ch in text if ch not in exclude)
     print(text)
     nlp = spacy.load("en")
     doc = nlp(text)

     ner_location = []
     ner_person = []
     ner_org = []

     for token in doc.ents:
         if token.label_ == 'LOC' or token.label_ == 'GPE' or token.label_ == 'FAC':
             ner_location.append(token)
         elif token.label_ == 'PERSON':
             ner_person.append(token.text)
         elif token.label_ == 'ORG':
            ner_org.append(token.text)
     print(ner_org)
#     ner_location = get_continuous_chunks(sentence, 'GPE')
#     ner_person = get_continuous_chunks(sentence, 'PERSON')
#     ner_organization = get_continuous_chunks(sentence, 'ORGANIZATION')
#
     location = ', '.join([str(elem) for elem in ner_location])

     person = ' ,'.join([str(elem) for elem in ner_person])
     org = ' ,'.join([str(elem) for elem in ner_org])
#
#
     location_list.append(location)
     person_list.append(person)
     org_list.append(org)
#     organization_list.append(organization)
     count = count + 1
     print(count)
#
#
data['Spacy Location'] = location_list
data['Spacy Person'] = person_list
data['Spacy Organization'] = org_list
# data['NLTK organization'] = organization_list

writefile = datapath / 'data/hugh-murray/chapter2/chapter2-spacy.csv'

data.to_csv(writefile, sep=str('\t'), encoding='latin1')