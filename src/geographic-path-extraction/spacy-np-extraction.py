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

sentence = "In that province there is a grand city named Teflis, with suburbs and fortified posts around it."

tree_str = nlp.parse(sentence)
#nps = extract_phrase(tree_str, 'NP')
vps = extract_phrase(tree_str, 'VP')
#pps = extract_phrase(tree_str, 'PP')

#print(nps)
#print("================================")
#print(vps)
#print("================================")
#print(pps)
#print("================================")

#print("******************************")
#for vp in vps:
#    print(vp)
#print("******************************")
verb = 'named'
verb_phrases = [i for i in vps if i.startswith(verb)]
print("==========================================================================")
print(verb_phrases)
# print("=================")
if len(verb_phrases) > 1:
    for verb_phrase in verb_phrases:
        temp_verb_phrases = []
        temp_verb_phrases = verb_phrases.copy()
        temp_verb_phrases.remove(verb_phrase)
#
        if not len(temp_verb_phrases) == 0:
             if any(verb_phrase in s for s in temp_verb_phrases):
                verb_phrases.remove(verb_phrase)
print("***************************")

print(verb_phrases)
for phrase in verb_phrases:
    tree_str = nlp.parse(phrase)
    nps = extract_phrase(tree_str, 'NP')
    print(nps)

# for verb_phrase in verb_phrases:
#     verb_phrase_changed = verb_phrase.replace(verb, "")
#     #print(verb_phrase_changed)
#     verb_phrase_changed = verb_phrase_changed.strip()
#     if verb_phrase_changed in nps:
#         found_nps.append(verb_phrase)
#
#     elif verb_phrase_changed in pps:
#         found_nps.append(verb_phrase)
# nlp.close()