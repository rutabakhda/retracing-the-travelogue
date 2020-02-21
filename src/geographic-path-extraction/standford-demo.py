from stanfordcorenlp import StanfordCoreNLP
import pandas as pd
from pathlib import Path
import json
import os

nlp = StanfordCoreNLP('/home/newo1347/PycharmProjects/ruta-thesis/tools/stanford-corenlp-full-2018-10-05')

def is_travelled_location(dependencies,verb_list,location):
    #found_match = []
    #for verb in verb_list:
    #    match = [location for item in dependencies if(item['governorGloss'] == verb and item['dependentGloss'] == location)]
    #    if match:
    #        found_match = found_match + match
    #print(found_match)
    for verb in verb_list:
        matched_list = get_relation(dependencies,verb)
        if location in matched_list:
            print("Match found")
        #else:


def get_relation(dependencies,word):
    match = []
    for item in dependencies:
        if item['governorGloss'] == word:
            match.append(item['dependentGloss'])
            return match



sentence =  "Now, let us leave them, and speak of Armenia the Greater."

output = nlp.annotate(sentence, properties={"outputFormat": "json", "annotators": "depparse"})
print(output)
res = json.loads(output)
#print(res)
res_dict = res['sentences'][0]
dependencies = res_dict['enhancedPlusPlusDependencies']

location_list = ['India','Chisi','Indian sea']
for location in location_list:
    narrate_verbs = 'sail'
    narrate_words_list = narrate_verbs.split(",")
    narrate_words_list = [item.strip() for item in narrate_words_list]
    matched_narrate_location = is_travelled_location(dependencies, narrate_words_list, location)

    #print("Matched Narrate Location = %s" % matched_narrate_location)