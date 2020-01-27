#!/usr/bin/env python3
from allennlp.predictors.predictor import Predictor
from pathlib import Path
import pandas as pd

datapath = Path(__file__).resolve().parents[2]
# Input individual index files
readfile = datapath / 'data/hugh-murray/chapter2/chapter2.csv'
data = pd.read_csv(readfile,sep=',', encoding='latin1',error_bad_lines=False)

predictor = Predictor.from_path(datapath / 'tools/fine-grained-ner-model-elmo-2018.12.21.tar.gz')
count = 0
location_list = []
person_list = []
organization_list = []

for index,row in data.iterrows():
    sentence = row['sentence']
    result = predictor.predict(sentence)

    tags = result['tags']
    words = result['words']

    entity_list = [i for i, value in enumerate(result['tags']) if value != 'O']

    ner_location = [words[item] + words[item+1] + words[item+2] for item in entity_list if tags[item].startswith("B-GPE")]
    ner_gpe = [words[item] for item in entity_list if tags[item].startswith("U-GPE")]
    ner_person_fullname = [words[item] + " " + words[item+1]  for item in entity_list if tags[item].startswith("B-PERSON")]
    ner_person = [words[item]  for item in entity_list if tags[item].startswith("U-PERSON")]
    ner_org = [words[item] for item in entity_list if tags[item].startswith("U-NORP")]

    all_location = ner_location + ner_gpe
    all_person = ner_person_fullname + ner_person

    location = ', '.join([str(elem) for elem in all_location])
    person = ' ,'.join([str(elem) for elem in all_person])
    organization = ' ,'.join([str(elem) for elem in ner_org])

    location_list.append(location)
    person_list.append(person)
    organization_list.append(organization)
    count = count + 1
    print(count)

data['allenNLP Location'] = location_list
data['allenNLP Person'] = person_list
data['allenNLP organization'] = organization_list

writefile = datapath / 'data/hugh-murray/chapter2/chapter2-allenNLP.csv'

data.to_csv(writefile, sep='\t', encoding='latin1')




