
from nltk.stem.wordnet import WordNetLemmatizer
from pathlib import Path
import pandas as pd
import os
import pickle
from nltk.corpus import framenet as fn
from stanfordcorenlp import StanfordCoreNLP

datapath = Path(__file__).resolve().parents[2]
nlp = StanfordCoreNLP('/home/newo1347/PycharmProjects/ruta-thesis/tools/stanford-corenlp-full-2018-10-05')

travel_verb_list = []

with open(datapath / "results/travel-verb-list.txt", "r") as f:   #Pickling
    for line in f:
        travel_verb_list.append(line.strip())

print(travel_verb_list)

def word_similarity(word):
    match_found = False
    if word in travel_verb_list:
        match_found = True

    return match_found


def find_verbs(sentence):
    pos = nlp.pos_tag(sentence)
        #print(pos)
    verbs_list = [item[0] for item in pos if item[1] in {'VB','VBD','VBG','VBN'}]
    return verbs_list

def find_travel_verbs(data):

    count = 0
    travel_verbs_final_list = []

    for index, row in data.iterrows():
        sentence = row['sentence']
        #verbs = row['Narrate verbs']
        found_verbs = find_verbs(sentence)
        travel_list = []

        for verb in found_verbs:
            base_verb = WordNetLemmatizer().lemmatize(verb, 'v')
            is_travel_verb = word_similarity(base_verb)

            if is_travel_verb:
                travel_list.append(verb)

        travel = ','.join(travel_list)
        travel_verbs_final_list.append(travel)
        count = count + 1
        print(count)

    data['Paper Travel'] = travel_verbs_final_list
    return data



book = ['part2']

for part in book:

    readfile = datapath / 'results/hugh-murray/{}/processed/{}-annotated-verbs1.csv'.format(part,part)
    data = pd.read_csv(readfile, sep='\t', encoding='latin1', error_bad_lines=False)

    outdata = find_travel_verbs(data)

    writefile = datapath / 'results/hugh-murray/{}/processed/{}-annotated-verbs1.csv'.format(part,part)
    if os.path.exists(writefile):
        os.remove(writefile)

    outdata.to_csv(writefile, sep='\t', encoding='latin1',index=False)

