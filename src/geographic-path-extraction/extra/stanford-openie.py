from stanfordcorenlp import StanfordCoreNLP
import pandas as pd
from pathlib import Path
import json
import os
from collections import Counter

def is_travelled_location(openie,verb):
    match = []
    found_match = []
    match = [item['object'] for item in openie if(item['relation'] == verb)]

    print(match)
    if len(match) > 1:
        match = list(set(match))
        match = [element.strip() for element in match]
        print(match)
        for ele in match:
            temp_match = []
            temp_match = match.copy()
            temp_match.remove(ele)
            
            if not len(temp_match) == 0:
                if any(ele in s for s in temp_match):
                    match.remove(ele)
                else:
                    found_match.append(ele)
    else:
        found_match = match

    print("===============================================================")
    return found_match

#nlp = StanfordCoreNLP('/home/newo1347/PycharmProjects/ruta-thesis/tools/stanford-corenlp-full-2018-10-05')
nlp = StanfordCoreNLP('/home/ruta/master-thesis/tools/stanford-corenlp-full-2018-10-05')

datapath = Path(__file__).resolve().parents[2]


def find_travelled_location(data):

    travel_list = []

    count = 0

    for index,row in data.iterrows():

        final_travel = []

        sentence = row['sentence']
        travel_verbs = row['Travel verbs']

        output = nlp.annotate(sentence, properties={"outputFormat": "json", "annotators": "openie"})
        res = json.loads(output)
        res_dict = res['sentences'][0]
        openie = res_dict['openie']

        if not isinstance(travel_verbs, float):
            travel_verbs_list = travel_verbs.split(",")


            for verb in travel_verbs_list:
               travel_objects = is_travelled_location(openie,verb)

               if len(final_travel) == 0:
                final_travel = final_travel + travel_objects
               else:
                final_travel.append("|")
                final_travel = final_travel + travel_objects


        travel = ' ,'.join([str(elem) for elem in final_travel])
        travel_list.append(travel)
        count = count + 1
        print(count)
        print("===========================================================")

    data['Travelled Object openie'] = travel_list

    return data


book = ['part1']

for part in book:

    readfile = datapath / 'results/hugh-murray/{}/geograhpic-path-extraction/{}-annotated-verbs.csv'.format(part,part)
    data = pd.read_csv(readfile, sep='\t', encoding='latin1', error_bad_lines=False)

    outdata = find_travelled_location(data)

    writefile = str(datapath) + '/results/hugh-murray/{}/geograhpic-path-extraction/{}-dependency-objects.csv'.format(part,part)
    if os.path.exists(writefile):
        os.remove(writefile)

    outdata.to_csv(writefile, sep='\t', encoding='latin1',index=False)


