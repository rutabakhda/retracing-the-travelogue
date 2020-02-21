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

sentence = "Did you not know that I was your enemy, and coming to attack you with this mighty host?"

tree_str = nlp.parse(sentence)
nps = extract_phrase(tree_str, 'NP')
vps = extract_phrase(tree_str, 'VP')
pps = extract_phrase(tree_str, 'PP')

print(nps)
print("================================")
print(vps)
print("================================")
print(pps)
print("================================")

nlp.close()