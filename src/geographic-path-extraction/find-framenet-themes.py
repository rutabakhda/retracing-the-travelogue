#!/usr/bin/env python3

from stanfordcorenlp import StanfordCoreNLP
import pandas as pd
from pathlib import Path
import os
import json

#nlp = StanfordCoreNLP('/home/newo1347/PycharmProjects/ruta-thesis/tools/stanford-corenlp-full-2018-10-05')
nlp = StanfordCoreNLP('/home/ruta/master-thesis/tools/stanford-corenlp-full-2018-10-05')
datapath = Path(__file__).resolve().parents[2]

def find_subject(sentence,verb,dependencies):
    match_list = []
    match_list2 = []

    match_list = [item['dependentGloss'] for item in dependencies if ((item['governorGloss'] == verb) & (item['dep'] == 'dobj'))]

    for item in match_list:
        match_list2 = [item['dependentGloss'] for item in dependencies if((item['governorGloss'] == item) & (item['dep'] == 'nmod:of'))]

    match = ",".join(match_list2)
    return match

def find_themes(data):
    count = 0
    subj_list = []

    for index,row in data.iterrows():
        sentence = row['sentence']
        travel_verbs = row['Travel verbs']

        print(sentence)
        temp_list = []
        if not isinstance(travel_verbs,float):

            output = nlp.annotate(sentence, properties={"outputFormat": "json", "annotators": "depparse"})
            # print(output)
            res = json.loads(output)
            # print(res)
            res_dict = res['sentences'][0]
            dependencies = res_dict['enhancedPlusPlusDependencies']

            travel_verbs_list = travel_verbs.split(",")

            for verb in travel_verbs_list:
                subj = find_subject(sentence,verb,dependencies)
                temp_list.append(subj)

        temp = ",".join(temp_list)
        subj_list.append(temp)


    data['Verb object'] = subj_list

    return data


def make_sentence(data):
    count = 0
    temp_list = []

    for index,row in data.iterrows():
        sentence = row['sentence']
        travel_verbs = row['Travel verbs']
        #verb_subject = row['Verb subject']
        verb_object = row['Verb object']

        sentence_token = sentence.split(" ")
        print(sentence_token)


        if not isinstance(travel_verbs,float):

            travel_verbs_list = travel_verbs.split(",")
            print(travel_verbs_list)

            if len(travel_verbs_list) == 1:
                if travel_verbs in sentence_token:
                    verb_index = sentence_token.index(travel_verbs)
                    sentence_token[verb_index] = '<motion-vb fn-frame=" ">'+travel_verbs+'</motion-vb>'

                    if verb_object in sentence_token:
                        object_index = sentence_token.index(verb_object)
                        sentence_token[object_index] = '<loc fe="destination">' + verb_object + '</loc>'

        tagged_sentence = " ".join(sentence_token)
        print(tagged_sentence)
        print("=======================")
        temp_list.append(tagged_sentence)
        count = count + 1


                #if verb_subject in sentence_token:
                #if verb_object in sentence_token:
                #    print("yes")

                #    subject_index = sentence_token.index(verb_subject)
                #    object_index = sentence_token.index(verb_object)
            #for verb in travel_verbs_list:
                #subj = find_subject(sentence,verb,dependencies)
                #temp_list.append(subj)

        #temp = ",".join(temp_list)
        #subj_list.append(temp)


    print(len(temp_list))
    data['Tagged sentence'] = temp_list
        #print("=========================")

    return data



#book = ['part1','part2','part3']
book = ['part1']

for part in book:

    readfile = datapath / 'results/hugh-murray/{}/geograhpic-path-extraction/{}-annotated-subj.csv'.format(part,part)
    data = pd.read_csv(readfile, sep='\t', encoding='latin1', error_bad_lines=False)

    outdata = make_sentence(data)

    nlp.close()

    outdir = str(datapath) + '/results/hugh-murray/{}/geograhpic-path-extraction'.format(part)

    if not os.path.isdir(outdir):
        os.makedirs(outdir)

    writefile = str(datapath) + '/results/hugh-murray/{}/geograhpic-path-extraction/{}-annotated-sentences.csv'.format(part,part)
    if os.path.exists(writefile):
        os.remove(writefile)

    outdata.to_csv(writefile, sep='\t', encoding='latin1',index=False)

