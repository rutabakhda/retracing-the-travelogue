#!/usr/bin/env python3

# from pathlib import Path
# # Simple usage
# from stanfordcorenlp import StanfordCoreNLP
#
# datapath = Path(__file__).resolve().parent.parent.parent
#
# print(datapath / 'tools/stanford-corenlp-full-2018-10-05')
# print("==================================================================")
# nlp = StanfordCoreNLP('/home/newo1347/PycharmProjects/ruta-thesis/tools/stanford-corenlp-full-2018-10-05')
#
# sentence = 'Guangdong University of Foreign Studies is located in Guangzhou.'
# print ('Tokenize:', nlp.word_tokenize(sentence))
# print ('Part of Speech:', nlp.pos_tag(sentence))
# print ('Named Entities:', nlp.ner(sentence))
# print ('Constituency Parsing:', nlp.parse(sentence))
# print ('Dependency Parsing:', nlp.dependency_parse(sentence))

#nlp.close() # Do not forget to close! The backend server will consume a lot memery.

from stanfordcorenlp import StanfordCoreNLP
from nltk.tree import Tree
import pandas as pd
from pathlib import Path
import os

nlp = StanfordCoreNLP('/home/newo1347/PycharmProjects/ruta-thesis/tools/stanford-corenlp-full-2018-10-05')


datapath = Path(__file__).resolve().parents[2]

def extract_phrase(tree_str, label):
    phrases = []
    trees = Tree.fromstring(tree_str)
    for tree in trees:
        for subtree in tree.subtrees():
            if subtree.label() == label:
                t = subtree
                t = ' '.join(t.leaves())
                phrases.append(t)

    return phrases


def find_travel_phrase(data):
    count = 0
    travel_phrase_vp_list = []
    travel_phrase_np_list = []

    for index,row in data.iterrows():
        sentence = row['sentence']
        travel_verbs_str = row['Travel verbs']
        if not isinstance(travel_verbs_str,float):
         travel_verbs = travel_verbs_str.split(",")
        else:
            travel_verbs = []

        tree_str = nlp.parse(sentence)
        #nps = extract_phrase(tree_str, 'NP')
        vps = extract_phrase(tree_str, 'VP')
        #pps = extract_phrase(tree_str, 'PP')

        found_vps = []
        found_nps = []

        for verb in travel_verbs:
            verb_phrases = [i for i in vps if i.startswith(verb)]
            nps = []

            if len(verb_phrases) > 1:
                for verb_phrase in verb_phrases:
                    temp_verb_phrases = []
                    temp_verb_phrases = verb_phrases.copy()
                    temp_verb_phrases.remove(verb_phrase)
                    #
                    if not len(temp_verb_phrases) == 0:
                        if any(verb_phrase in s for s in temp_verb_phrases):
                            verb_phrases.remove(verb_phrase)

            print(len(verb_phrases))
            for verb_phrase in verb_phrases:
                tree_str = nlp.parse(verb_phrase)
                nps = extract_phrase(tree_str, 'NP')

            found_vps = found_vps + verb_phrases
            found_nps = found_nps + nps

            # for verb_phrase in verb_phrases:
            #      verb_phrase_changed = verb_phrase.replace(verb, "")
            #      print(verb_phrase_changed)
            #      verb_phrase_changed = verb_phrase_changed.strip()
            #      if verb_phrase_changed in nps:
            #          found_nps.append(verb_phrase)
            #
            #      elif verb_phrase_changed in pps:
            #          found_nps.append(verb_phrase)

        vps = ','.join(found_vps)
        nps = ','.join(found_nps)
        travel_phrase_vp_list.append(vps)
        travel_phrase_np_list.append(nps)
        count = count + 1
        print(count)
        print("===============================")


    data['Travel Verb Phrases'] = travel_phrase_vp_list
    data['Travel Noun Phrases'] = travel_phrase_np_list
    nlp.close()
    return data

book = ['part2']

for part in book:

    readfile = datapath / 'results/hugh-murray/{}/geograhpic-path-extraction/{}-annotated-with-verbs.csv'.format(part, part)
    data = pd.read_csv(readfile, sep='\t', encoding='latin1', error_bad_lines=False)

    outdata = find_travel_phrase(data)

    writefile = datapath / 'results/hugh-murray/{}/geograhpic-path-extraction/{}-np-phrases.csv'.format(part, part)
    if os.path.exists(writefile):
        os.remove(writefile)

    outdata.to_csv(writefile, sep='\t', encoding='latin1', index=False)



