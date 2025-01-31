from stanfordcorenlp import StanfordCoreNLP
import pandas as pd
from pathlib import Path
import json
import os
from collections import Counter

def is_travelled_location(dependencies,verb_list,location):
    found_match = []
    for verb in verb_list:
        match = [item['dependentGloss'] for item in dependencies if(item['governorGloss'] == verb)]
        print(verb)
        print(match)
        print("===============================================================")
        if match:
            if location in match:
                found_match.append(location)
    return found_match

#nlp = StanfordCoreNLP('/home/newo1347/PycharmProjects/ruta-thesis/tools/stanford-corenlp-full-2018-10-05')
nlp = StanfordCoreNLP('/home/ruta/master-thesis/tools/stanford-corenlp-full-2018-10-05')

datapath = Path(__file__).resolve().parents[2]


def find_travelled_location(data):
    narrate_list = []
    travel_list = []
    travel_phrase_list = []
    count = 0

    for index,row in data.iterrows():

        verb_phrases = []
        travel_verb_phrases = []
        travel_verbs_list = []
        narrate_verb_phrases = []
       
        travel_phrases = row['Travel Noun Phrases']

        if not isinstance(travel_phrases,float):
            travel_verb_phrases = travel_phrases.split(",")

        verb_phrases = travel_verb_phrases
        print(verb_phrases)
        location = row['Location']

        travel_verbs = row['Location']
        if not isinstance(travel_verbs, float):
            travel_verbs_list = travel_verbs.split(",")

        matched_narrate_list = []
        matched_travel_list = []
        matched_travel_phrase = []
 
        for sentence in verb_phrases:
            sentence_list = sentence.split(" ")
            print(sentence_list)
            common_travel = (list((Counter(sentence_list) & Counter(travel_verbs_list)).elements()))
            print(common_travel)
            if len(common_travel) != 0:
                matched_travel_list = matched_travel_list + common_travel
                matched_travel_phrase.append(sentence)



        final_travel = matched_travel_list
        travel = ' ,'.join([str(elem) for elem in final_travel])
        travel_phrase = ' ,'.join([str(elem) for elem in matched_travel_phrase])

        travel_phrase_list.append(travel_phrase)
        travel_list.append(travel)
        count = count + 1
        print(count)
        print("===========================================================")

    data['Travel Phrases'] = travel_phrase_list
    data['Travelled Location'] = travel_list

    return data


book = ['part1']

for part in book:

    readfile = datapath / 'results/hugh-murray/{}/geograhpic-path-extraction/{}-np-phrases-voted-annotated.csv'.format(part,part)
    data = pd.read_csv(readfile, sep='\t', encoding='latin1', error_bad_lines=False)

    outdata = find_travelled_location(data)

    writefile = str(datapath) + '/results/hugh-murray/{}/geograhpic-path-extraction/{}-np-phrases-travel-voted-annotated.csv'.format(part,part)
    if os.path.exists(writefile):
        os.remove(writefile)

    outdata.to_csv(writefile, sep='\t', encoding='latin1',index=False)


