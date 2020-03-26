#!/usr/bin/env python3

from stanfordcorenlp import StanfordCoreNLP
import pandas as pd
from pathlib import Path
import os

#nlp = StanfordCoreNLP('/home/newo1347/PycharmProjects/ruta-thesis/tools/stanford-corenlp-full-2018-10-05')
nlp = StanfordCoreNLP('/home/ruta/master-thesis/tools/stanford-corenlp-full-2018-10-05')


datapath = Path(__file__).resolve().parents[2]

def find_verbs(data):

    verbs_final_list = []
    count = 0

    for index,row in data.iterrows():
        sentence = row['sentence']
        print(sentence)
        pos = nlp.pos_tag(sentence)
        #print(pos)

        verbs_list = [item[0] for item in pos if item[1] in {'VB','VBD','VBG','VBN'}]
        verbs = ','.join(verbs_list)

        verbs_final_list.append(verbs)
        count = count + 1
        print(count)


    data['Travel verbs'] = verbs_final_list
    data['Narrate verbs'] = verbs_final_list

    return data

book = ['part1','part2','part3']
#book = ['part2']

for part in book:

    readfile = datapath / 'results/hugh-murray/{}/processed/{}-annotated.csv'.format(part,part)
    data = pd.read_csv(readfile, sep='\t', encoding='latin1', error_bad_lines=False)

    outdata = find_verbs(data)

    outdir = str(datapath) + '/results/hugh-murray/{}/geograhpic-path-extraction'.format(part)

    if not os.path.isdir(outdir):
        os.makedirs(outdir)

    writefile = str(datapath) + '/results/hugh-murray/{}/geograhpic-path-extraction/{}-annotated-verbs.csv'.format(part,part)
    if os.path.exists(writefile):
        os.remove(writefile)

    outdata.to_csv(writefile, sep='\t', encoding='latin1',index=False)


