#WordNet as thesaurus
from nltk.corpus import wordnet as wn
from itertools import product
from nltk.stem.wordnet import WordNetLemmatizer
from pathlib import Path
import pandas as pd
import os
import nltk
import re
from nltk.corpus import verbnet as vn

#from stanfordcorenlp import StanfordCoreNLP

datapath = Path(__file__).resolve().parents[2]
#nlp = StanfordCoreNLP('/home/newo1347/PycharmProjects/ruta-thesis/tools/stanford-corenlp-full-2018-10-05')

travel_verbs = ['depart','travel','arrive']

def word_similarity(word):
    match_found = False
    vn_results = vn.classids(lemma=word)
    for item in vn_results:
        #x = re.search("51.1|51.4.2", item)
        x = re.search("51",item)
        if x is not None:
            match_found = True

    return match_found



#def find_verbs(sentence):
    #pos = nlp.pos_tag(sentence)
        #print(pos)
    #verbs_list = [item[0] for item in pos if item[1] in {'VB','VBD','VBG','VBN'}]
    #return verbs_list

def find_travel_verbs(data):

    count = 0
    travel_verbs_final_list = []

    for index, row in data.iterrows():
        sentence = row['sentence']
        verbs = row['Narrate verbs']

        if not isinstance(verbs,float):
            found_verbs = verbs.split(",")
            #found_verbs = find_verbs(sentence)
            travel_list = []

            for verb in found_verbs:
                base_verb = WordNetLemmatizer().lemmatize(verb, 'v')
                is_travel_verb = word_similarity(base_verb)

                if is_travel_verb:
                    travel_list.append(verb)

            travel = ','.join(travel_list)

            travel_verbs_final_list.append(travel)
        else:
            travel = []
            travel_verbs_final_list.append(travel)

        count = count + 1
        print(count)

    data['VerbNet Travel'] = travel_verbs_final_list
    return data



book = ['part2']

for part in book:

    readfile = datapath / 'results/hugh-murray/{}/processed/{}-annotated-wordnet.csv'.format(part,part)
    data = pd.read_csv(readfile, sep='\t', encoding='latin1', error_bad_lines=False)

    outdata = find_travel_verbs(data)

    writefile = datapath / 'results/hugh-murray/{}/processed/{}-annotated-verbnet.csv'.format(part,part)
    if os.path.exists(writefile):
        os.remove(writefile)

    outdata.to_csv(writefile, sep='\t', encoding='latin1')

