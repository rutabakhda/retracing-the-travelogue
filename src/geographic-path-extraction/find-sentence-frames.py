from nltk.corpus import verbnet as vn
from pathlib import Path
import pandas as pd
import os
import re
import nltk
from stanfordcorenlp import StanfordCoreNLP
from nltk.tree import Tree

#nltk.download('verbnet')
nlp = StanfordCoreNLP('/home/ruta/master-thesis/tools/stanford-corenlp-full-2018-10-05')

grammar = r'''NVN:{<NP><VB.*><NP>'''

def extract_phrase(tree_str, label):
    phrases = []
    trees = Tree.fromstring(tree_str)
    for tree in trees:
        #print(tree)
        #print("#########################")
        for subtree in tree.subtrees():
            #print(subtree)
            if subtree.label() == label:
                t = subtree
                t = ' '.join(t.leaves())
                phrases.append(t)

    return phrases

sentence = "for thither all the spices, rich cloths, and other precious articles, are brought from India across the Euphrates, which the merchants of Venice, of Pisa, and of Genoa, come to purchase."


before_verb = "for thither all the spices, rich cloths, and other precious articles, are brought from India across the Euphrates, which the merchants of Venice, of Pisa, and of Genoa"
after_verb = "to purchase"



tree_str = nlp.parse(sentence)


nps = extract_phrase(tree_str, 'NP')
vps = extract_phrase(tree_str, 'VP')
pps = extract_phrase(tree_str, 'PP')

if before_verb in nps:
    print("YES BEFORE VERB")

if after_verb in nps:
    print("YES AFTER VERB")


print(nps)
print(vps)
print(pps)

for np in nps:
    print(np)

print("=============")

word = "come"
vn_results = vn.classids(lemma=word)
print(vn_results)

frames = vn.frames('51.2')[0]


syntax = frames['syntax']
for item in syntax:
    print(item['pos_tag'])
    print("=====================")
nlp.close()