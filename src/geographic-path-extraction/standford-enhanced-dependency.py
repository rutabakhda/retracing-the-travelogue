from stanfordcorenlp import StanfordCoreNLP
import pandas as pd
from pathlib import Path
import json
import os

def is_travelled_location(dependencies,verb_list,location):
    found_match = []
    for verb in verb_list:
        match = [location for item in dependencies if(item['governorGloss'] == verb and item['dependentGloss'] == location)]
        if match:
            found_match = found_match + match
    return found_match

nlp = StanfordCoreNLP('/home/newo1347/PycharmProjects/ruta-thesis/tools/stanford-corenlp-full-2018-10-05')

datapath = Path(__file__).resolve().parents[2]


def find_travelled_location(data):
    narrate_list = []
    travel_list = []
    count = 0

    for index,row in data.iterrows():

        sentence = row['Narrate Phrases']
        location = row['Location']

        #is_narrate = row['Is Narrate']
        #is_travel = row['Is Travel']
        #narrate_verbs = row['Narrate Verbs']
        #travel_verbs = row['Travel Verbs']
        travel_verbs = row['Travel verbs']
        narrate_verbs = row['Narrate verbs']

        matched_narrate_list = []
        matched_travel_list = []

        if not isinstance(location,float) and not isinstance(sentence,float):
            output = nlp.annotate(sentence, properties={"outputFormat": "json", "annotators": "depparse"})
            res = json.loads(output)
            res_dict = res['sentences'][0]
            dependencies = res_dict['enhancedDependencies']

            location_list = location.split(",")

            for location in location_list:
                if not isinstance(narrate_verbs, float):
                     narrate_words_list = narrate_verbs.split(",")
                     matched_narrate_location = is_travelled_location(dependencies,narrate_words_list,location)
                     if matched_narrate_location:
                         matched_narrate_list = matched_narrate_list + matched_narrate_location

                if not isinstance(travel_verbs, float):
                    travel_words_list = travel_verbs.split(",")
                    matched_travel_location = is_travelled_location(dependencies,travel_words_list, location)
                    if matched_travel_location:
                        matched_travel_list = matched_travel_list + matched_travel_location


        final_travel = matched_narrate_list + matched_travel_list

        #narrate = ', '.join([str(elem) for elem in matched_narrate_list])
        travel = ' ,'.join([str(elem) for elem in final_travel])

        #narrate_list.append(narrate)
        travel_list.append(travel)
        count = count + 1
        print(count)

    #data['Narrate Location'] = narrate_list
    data['Travelled Location'] = travel_list

    return data


book = ['part2']

for part in book:

    readfile = datapath / 'results/hugh-murray/{}/geograhpic-path-extraction/{}-np-phrases.csv'.format(part,part)
    data = pd.read_csv(readfile, sep='\t', encoding='latin1', error_bad_lines=False)

    outdata = find_travelled_location(data)

    writefile = datapath / 'results/hugh-murray/{}/geograhpic-path-extraction/{}-np-phrases.csv'.format(part,part)
    if os.path.exists(writefile):
        os.remove(writefile)

    outdata.to_csv(writefile, sep='\t', encoding='latin1',index=False)


