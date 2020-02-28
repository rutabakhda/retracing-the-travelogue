from stanfordcorenlp import StanfordCoreNLP
import pandas as pd
from pathlib import Path
import json
import os
from collections import Counter

def is_travelled_location(dependencies,verb_list,location):
    found_match = []
    for verb in verb_list:
        match = [item['dependentGloss']  for item in dependencies if(item['governorGloss'] == verb)]
        if match:
            if location in match:
                found_match.append(location)
    return found_match

nlp = StanfordCoreNLP('/home/newo1347/PycharmProjects/ruta-thesis/tools/stanford-corenlp-full-2018-10-05')

datapath = Path(__file__).resolve().parents[2]


def find_travelled_location(data):
    narrate_list = []
    travel_list = []
    travel_phrase_list = []
    count = 0

    for index,row in data.iterrows():

        verb_phrases = []
        #sentence = row['Travel Noun Phrases']
        phrases = row['Travel Noun Phrases']
        if not isinstance(phrases,float):
            verb_phrases = phrases.split(",")
        location = row['Location']

        #is_narrate = row['Is Narrate']
        #is_travel = row['Is Travel']
        #narrate_verbs = row['Narrate Verbs']
        #travel_verbs = row['Travel Verbs']

        travel_verbs = row['Location']
        if not isinstance(travel_verbs, float):
            travel_verbs_list = travel_verbs.split(",")
       # narrate_verbs = row['Narrate verbs']
       # if not isinstance(narrate_verbs, float):
       #     narrate_verbs_list = narrate_verbs.split(",")

        matched_narrate_list = []
        matched_travel_list = []
        matched_travel_phrase = []

        if len(verb_phrases) > 1:
            new_verb_phrase = []
            for verb_phrase in verb_phrases:
                #print(verb_phrases)
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

        for sentence in new_verb_phrase:
            sentence_list = sentence.split(" ")
            #print(sentence_list)
            common_travel = (list((Counter(sentence_list) & Counter(travel_verbs_list)).elements()))
            #print(common_travel)
            if len(common_travel) != 0:
                matched_travel_list = matched_travel_list + common_travel
                matched_travel_phrase.append(sentence)



        final_travel = matched_travel_list
        #print(final_travel)

        #narrate = ', '.join([str(elem) for elem in matched_narrate_list])
        travel = ' ,'.join([str(elem) for elem in final_travel])
        travel_phrase = ' ,'.join([str(elem) for elem in matched_travel_phrase])

        #narrate_list.append(narrate)
        travel_phrase_list.append(travel_phrase)
        travel_list.append(travel)
        count = count + 1
        print(count)

    data['Travel Phrases'] = travel_phrase_list
    data['Travelled Location'] = travel_list

    return data


book = ['part2']

for part in book:

    readfile = datapath / 'results/hugh-murray/{}/geograhpic-path-extraction/{}-np-phrases.csv'.format(part,part)
    data = pd.read_csv(readfile, sep='\t', encoding='latin1', error_bad_lines=False)

    outdata = find_travelled_location(data)

    writefile = datapath / 'results/hugh-murray/{}/geograhpic-path-extraction/{}-np-phrases.travel.csv'.format(part,part)
    if os.path.exists(writefile):
        os.remove(writefile)

    outdata.to_csv(writefile, sep='\t', encoding='latin1',index=False)


