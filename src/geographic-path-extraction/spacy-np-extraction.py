
from stanfordcorenlp import StanfordCoreNLP
from nltk.tree import Tree
import pandas as pd
from pathlib import Path
import os

nlp = StanfordCoreNLP('/home/ruta/master-thesis/tools/stanford-corenlp-full-2018-10-05')


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

def my_nth_txt(text, n):
    return text.split()[n]

sentence = "and entering the church, they sung the holy mass, and then proceeded out to the plain in front of the mountain."

tree_str = nlp.parse(sentence)
nps = extract_phrase(tree_str, 'NP')
vps = extract_phrase(tree_str, 'VP')
pps = extract_phrase(tree_str, 'PP')

print(nps)
#print("================================")
#print(vps)
#print("================================")
print(pps)
#print("================================")

#print("******************************")
#for vp in vps:
#    print(vp)
#print("******************************")
verb = 'proceed'
verb_phrases = [i for i in vps if i.startswith(verb)]
print("==========================================================================")
print(verb_phrases)
# print("=================")
new_noun_phrase = []
new_noun_phrase1 = []
new_verb_phrase = []
new_prep_phrase = []

if len(verb_phrases) > 1:

    for verb_phrase in verb_phrases:
        temp_verb_phrases = []
        temp_verb_phrases = verb_phrases.copy()
        temp_verb_phrases.remove(verb_phrase)
#
        if not len(temp_verb_phrases) == 0:
             if any(verb_phrase in s for s in temp_verb_phrases):
                verb_phrases.remove(verb_phrase)
             else:
                 new_verb_phrase.append(verb_phrase)
else:
    new_verb_phrase = verb_phrases


for phrase in new_verb_phrase:
    tree_str = nlp.parse(phrase)
    nps = extract_phrase(tree_str, 'NP')
    pps = extract_phrase(tree_str, 'PP')

    word_after_verb = my_nth_txt(phrase,1)
    print(word_after_verb)

    noun_phrases = [i for i in nps if i.startswith(word_after_verb)]

    if len(noun_phrases) > 1:

        for noun_phrase in noun_phrases:
            temp_noun_phrases = []
            temp_noun_phrases = noun_phrases.copy()
            temp_noun_phrases.remove(noun_phrase)
            #
            if not len(temp_noun_phrases) == 0:
                if any(noun_phrase in s for s in temp_noun_phrases):
                    noun_phrases.remove(noun_phrase)
                else:
                    new_noun_phrase.append(noun_phrase)
    else:
        new_noun_phrase = noun_phrases




    prep_phrases = [i for i in pps if i.startswith(word_after_verb)]

    if len(prep_phrases) > 1:

        for prep_phrase in prep_phrases:
            temp_prep_phrases = []
            temp_prep_phrases = prep_phrases.copy()
            temp_prep_phrases.remove(prep_phrase)
            #
            if not len(temp_prep_phrases) == 0:
                if any(prep_phrase in s for s in temp_prep_phrases):
                    prep_phrases.remove(prep_phrase)
                else:
                    new_prep_phrase.append(prep_phrase)
    else:
        new_prep_phrase = prep_phrases

    for phrase in new_prep_phrase:

        print("==========================")
        print(phrase)
        tree_str = nlp.parse(phrase)
        nps1 = extract_phrase(tree_str, 'NP')
        print(nps1)
        word_after_verb1 = my_nth_txt(phrase, 1)
        print(word_after_verb1)

        noun_phrases1 = [i for i in nps1 if i.startswith(word_after_verb1)]
        print(noun_phrases1)
        print('~~~~~~~~')
        if len(noun_phrases1) > 1:

            for noun_phrase1 in noun_phrases1:
                temp_noun_phrases1 = []
                temp_noun_phrases1 = noun_phrases1.copy()
                temp_noun_phrases1.remove(noun_phrase1)
                #
                if not len(temp_noun_phrases1) == 0:
                    if any(noun_phrase1 in s for s in temp_noun_phrases1):
                        noun_phrases1.remove(noun_phrase1)
                    else:
                        new_noun_phrase1.append(noun_phrase1)
        else:
            new_noun_phrase1 = noun_phrases1

print(new_noun_phrase)
print(new_prep_phrase)
print(new_noun_phrase1)

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