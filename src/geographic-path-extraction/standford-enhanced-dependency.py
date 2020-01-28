from stanfordcorenlp import StanfordCoreNLP
import pandas as pd
from pathlib import Path
import json

def is_travelled_location(dependencies,verb_list,location):
    found_match = []
    for verb in verb_list:
        match = [location for item in dependencies if(item['governorGloss'] == verb and item['dependentGloss'] == location)]
        if match:
            found_match = found_match + match
    return found_match

nlp = StanfordCoreNLP('/home/newo1347/PycharmProjects/ruta-thesis/tools/stanford-corenlp-full-2018-10-05')

datapath = Path(__file__).resolve().parents[2]
readfile = datapath / 'data/hugh-murray/chapter3/chapter3-find-travel.csv'
data = pd.read_csv(readfile,sep=',', encoding='latin1',error_bad_lines=False,nrows=1)

narrate_list = []
travel_list = []
count = 0

for index,row in data.iterrows():

    sentence = row['sentence']
    location = row['Location']
    is_narrate = row['Location']
    is_travel = row['Location']
    narrate_verbs = row['Location']
    travel_verbs = row['Location']

    if location:
        if is_narrate!= 0 or is_travel!=0 :
            output = nlp.annotate(sentence, properties={"outputFormat": "json", "annotators": "depparse"})
            res = json.loads(output)
            res_dict = res['sentences'][0]
            dependencies = res_dict['enhancedDependencies']

            location_list = location.split(",")

            matched_narrate_list = []
            matched_travel_list = []

            for location in location_list:
                if is_narrate!=0:
                    narrate_words_list = narrate_verbs.split(",")
                    matched_narrate_location = is_travelled_location(dependencies,narrate_words_list,location)
                    if matched_narrate_location:
                        matched_narrate_list = matched_narrate_list + matched_narrate_location
                if is_travel!=0:
                    travel_words_list = travel_verbs.split(",")
                    matched_travel_location = is_travelled_location(dependencies,narrate_words_list, location)
                    if matched_travel_location:
                        matched_travel_list = matched_travel_list + matched_travel_location

    narrate = ', '.join([str(elem) for elem in matched_narrate_list])
    travel = ' ,'.join([str(elem) for elem in matched_travel_list])

    narrate_list.append(narrate)
    travel_list.append(travel)
    count = count + 1
    print(count)

data['Narrate Location'] = narrate_list
data['Travelled Location'] = travel_list

writefile = datapath / 'data/hugh-murray/chapter3/chapter3-matched-travel.csv'

data.to_csv(writefile, sep=',', encoding='latin1')


