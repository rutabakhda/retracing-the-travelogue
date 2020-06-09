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
    leng = text.split()
    if len(leng) > n:
        return text.split()[n]
    return ""

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
        
        vps = extract_phrase(tree_str, 'VP')
        
        #print(vps)
        found_vps = []
        found_nps = []
        #print(travel_verbs)
        for verb in travel_verbs:
            print("*******************************************")
            print(verb)
            verb_phrases = [i for i in vps if i.startswith(verb)]
            #print(verb_phrases)
            nps = []
            new_verb_phrase = []
            new_noun_phrase = []
            new_noun_phrase1 = []
            new_prep_phrase = []
            
            if len(verb_phrases) == 0:
                #print("COMES HERE")
                split_sent = sentence.split(verb)
                #print(len(split_sent))
                if len(split_sent) > 1:
                  if split_sent[1].find(","):
                  #print("TRUE")
                    verb_sent = split_sent[1].split(",")
                  
                  else:				
                    verb_sent = split_sent[1].split(".")
                #print("**************")
                  created_vp_sent = verb_sent[0].strip()
                  created_vp = verb+" "+created_vp_sent
                  new_verb_phrase.append(created_vp)
                else:  
                  new_verb_phrase = verb_phrases
            elif len(verb_phrases) > 1:

                for verb_phrase in verb_phrases:
                    temp_verb_phrases = []
                    temp_verb_phrases = verb_phrases.copy()
                    temp_verb_phrases.remove(verb_phrase)
                    
                    if not len(temp_verb_phrases) == 0:
                        if any(verb_phrase in s for s in temp_verb_phrases):
                            verb_phrases.remove(verb_phrase)
                        else:
                            new_verb_phrase.append(verb_phrase)
            else:
                new_verb_phrase = verb_phrases
            #print("VERB PHRASES")
            #print(new_verb_phrase)
            for phrase in new_verb_phrase:
                phrase = "I " + phrase
                #print(phrase)
                tree_str = nlp.parse(phrase)
                nps = extract_phrase(tree_str, 'NP')
                pps = extract_phrase(tree_str, 'PP')
                #print(nps)
                #print(pps)
                #print("================")
                print(phrase)
                word_after_verb = my_nth_txt(phrase, 2)
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

                    #print("==========================")
                    #print(phrase)
                    tree_str = nlp.parse(phrase)
                    nps1 = extract_phrase(tree_str, 'NP')
                    #print(nps1)
                    word_after_verb1 = my_nth_txt(phrase, 1)
                    #print(word_after_verb1)

                    noun_phrases1 = [i for i in nps1 if i.startswith(word_after_verb1)]
                    #print(noun_phrases1)
                    #print('~~~~~~~~')
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



      


            found_vps = found_vps + new_verb_phrase
            found_nps = found_nps + new_noun_phrase + new_noun_phrase1
            #print("**************************************")
            print(found_vps)
            print(found_nps)

            # for verb_phrase in verb_phrases:
            #      verb_phrase_changed = verb_phrase.replace(verb, "")
            #      print(verb_phrase_changed)
            #      verb_phrase_changed = verb_phrase_changed.strip()
            #      if verb_phrase_changed in nps:
            #          found_nps.append(verb_phrase)
            #
            #      elif verb_phrase_changed in pps:
            #          found_nps.append(verb_phrase)
		#print(found_vps)
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

    rows_to_keep = [0,857]
    readfile = datapath / 'results/hugh-murray/{}/geograhpic-path-extraction/{}-annotated-verbs.csv'.format(part, part)
    data = pd.read_csv(readfile, sep='\t', encoding='latin1', error_bad_lines=False)
    #data = pd.read_csv(readfile, sep='\t', encoding='latin1', error_bad_lines=False,skiprows = lambda x: x not in rows_to_keep)

	#print(data)
    outdata = find_travel_phrase(data)
	
    writefile = str(datapath) + '/results/hugh-murray/{}/geograhpic-path-extraction/{}-np-phrases.csv'.format(part, part)

    if os.path.exists(writefile):
      os.remove(writefile)
	
    outdata.to_csv(writefile, sep='\t', encoding='latin1', index=False)



