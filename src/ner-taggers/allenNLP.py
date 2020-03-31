#!/usr/bin/env python3
from allennlp.predictors.predictor import Predictor
from pathlib import Path
import pandas as pd
import os

datapath = Path(__file__).resolve().parents[2]

predictor = Predictor.from_path(datapath / 'tools/fine-grained-ner-model-elmo-2018.12.21.tar.gz')

def tagger_allenNLP(data):
    count = 0
    location_list = []
    person_list = []
    organization_list = []

    for index,row in data.iterrows():
        #sentence = row['sentence']
        sentence = "Messer Marco Polo, of whom this book treats, governed it three years."
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

    return data

#book = ['part1','part2','part3']
book = ['part1']

for part in book:

    readfile = datapath / 'results/hugh-murray/{}/processed/{}-annotated-special.csv'.format(part,part)
    data = pd.read_csv(readfile, sep='\t', encoding='latin1', error_bad_lines=False,nrows=1)

    outdata = tagger_allenNLP(data)

    if not os.path.exists(datapath / 'results/hugh-murray/{}/ner'.format(part)):
       os.makedirs(datapath / 'results/hugh-murray/{}/ner'.format(part))

    writefile = datapath / 'results/hugh-murray/{}/ner/allenNLP.csv'.format(part)
    if os.path.exists(writefile):
        os.remove(writefile)

    outdata.to_csv(writefile, sep='\t', encoding='latin1',index=False)




