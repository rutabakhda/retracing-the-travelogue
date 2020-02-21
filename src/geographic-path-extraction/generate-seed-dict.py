import pandas as pd
from pathlib import Path
from nltk.corpus import wordnet as wn
import re

sense_key_regex = r"(.*)\%(.*):(.*):(.*):(.*):(.*)"
synset_types = {1:'n', 2:'v', 3:'a', 4:'r', 5:'s'}

def synset_from_sense_key(sense_key):
    lemma, ss_type, lex_num, lex_id, head_word, head_id = re.match(sense_key_regex, sense_key).groups()
    ss_idx = '.'.join([lemma, synset_types[int(ss_type)], lex_id])
    return wn.synset(ss_idx)


datapath = Path(__file__).resolve().parents[2]
readfile = datapath / 'tools/FnWnVerbMap.1.0.txt'

with open(readfile) as f:
    content = f.readlines()

travel_list = []
verb_list = []
#subs = ['arriving','departing','travel','motion','self_motion']
subs = ['arriving']
for sub in subs:
    res = [i for i in content if i.startswith(sub + " ")]
    travel_list = travel_list + res

for item in travel_list:

    item = item.strip()
    sense_key_list = item.split(" ")
    sense_key_list.pop(0)
    sense_key_list.pop(0)
    #print(sense_key_list)

    for sense_key in sense_key_list:
        sense = synset_from_sense_key(sense_key)
        lemmas = wn.synset(sense.name()).lemma_names()
        verb_list = verb_list + lemmas
        #print(wn.synset(sense.name()).lemma_names())

    #print("==============")


print(verb_list)
