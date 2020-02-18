#WordNet as thesaurus
from nltk.corpus import wordnet as wn
from itertools import product
from nltk.stem.wordnet import WordNetLemmatizer
from pathlib import Path
import pandas as pd
import os
import nltk

from stanfordcorenlp import StanfordCoreNLP

datapath = Path(__file__).resolve().parents[2]
nlp = StanfordCoreNLP('/home/newo1347/PycharmProjects/ruta-thesis/tools/stanford-corenlp-full-2018-10-05')

travel_verbs = ['depart','travel','arrive']

def word_similarity(wordx,wordy):
    vnet3 = nltk.corpus.util.LazyCorpusLoader('verbnet3', nltk.corpus.reader.verbnet.VerbnetCorpusReader,r'(?!\.).*\.xml')

    print(vnet3.classids('travel'))

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
        found_verbs = find_verbs(sentence)
        travel_list = []

        for verb in found_verbs:
            base_verb = WordNetLemmatizer().lemmatize(verb, 'v')
            max_score = 0

            for travel_verb in travel_verbs:
                score = word_similarity(travel_verb,base_verb)
                max_score = score if max_score < score else max_score
                print(score)

            if max_score > 0.5:
                travel_list.append(verb)

        travel = ','.join(travel_list)

        travel_verbs_final_list.append(travel)
        count = count + 1
        print(count)

    data['WordNet Travel'] = travel_verbs_final_list
    return data



book = ['part2']

for part in book:

    readfile = datapath / 'results/hugh-murray/{}/processed/{}-annotated-complete.csv'.format(part,part)
    data = pd.read_csv(readfile, sep='\t', encoding='latin1', error_bad_lines=False)

    outdata = find_travel_verbs(data)

    writefile = datapath / 'results/hugh-murray/{}/processed/{}-annotated-wordnet.csv'.format(part,part)
    if os.path.exists(writefile):
        os.remove(writefile)

    outdata.to_csv(writefile, sep='\t', encoding='latin1')

