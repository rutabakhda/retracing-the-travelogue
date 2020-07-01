import pandas as pd
from pathlib import Path
from nltk.corpus import wordnet as wn
import pickle
import os

datapath = Path(__file__).resolve().parents[2]
readfile = datapath / 'tools/FnWnVerbMap.1.0.txt'

with open(readfile) as f:
    content = f.readlines()

travel_list = []
verb_list = []
#subs1 = ['arriving','departing','travel','motion']
#subs = ['arriving','departing','travel']
subs = ['telling','statement']
#subs = ['departing']
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
        if sense_key is not '0':
            print(sense_key)
            print(type(wn.lemma_from_key(sense_key)))
            sense = wn.lemma_from_key(sense_key).synset()

            lemmas = wn.synset(sense.name()).lemma_names()
            verb_list = verb_list + lemmas

print(verb_list)

writefile = datapath / "results/narrate-verb-list.txt"
if os.path.exists(writefile):
    os.remove(writefile)

with open(writefile, "w") as f:   #Pickling
    for verb in verb_list:
        f.write(str(verb) + "\n")
