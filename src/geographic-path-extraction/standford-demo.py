from stanfordcorenlp import StanfordCoreNLP
import pandas as pd
from pathlib import Path
import json
import os

nlp = StanfordCoreNLP('/home/ruta/master-thesis/tools/stanford-corenlp-full-2018-10-05')

def is_travelled_location(dependencies,verb_list,location):
    #found_match = []
    for verb in verb_list:
        print(verb)
        match = [item['dependentGloss'] for item in dependencies if(item['governorGloss'] == verb)]
        if match:
            print(match)
            if location in match:
                print(location)

        else:
            print("MATCH NOT FOUND")
    #found_match = found_match + match
    #print(found_match)
    #for verb in verb_list:
    #    matched_list = get_relation(dependencies,verb)
    #    if location in matched_list:
    #        print("Match found")
        #else:


# def get_relation(dependencies,word):
#     match = []
#     for item in dependencies:
#         if item['governorGloss'] == word:
#             match.append(item['dependentGloss'])
#             return match



sentence =  "By this town we enter the province of Turcomania"

output = nlp.annotate(sentence, properties={"outputFormat": "json", "annotators": "depparse"})
#print(output)
res = json.loads(output)
#print(res)
res_dict = res['sentences'][0]
dependencies = res_dict['enhancedPlusPlusDependencies']

print(dependencies)

#location_list = ['Armenia the Greater']
#for location in location_list:
#    narrate_verbs = 'speak'
#   narrate_words_list = narrate_verbs.split(",")
#  narrate_words_list = [item.strip() for item in narrate_words_list]
#   matched_narrate_location = is_travelled_location(dependencies, narrate_words_list, location)
nlp.close()
    #print("Matched Narrate Location = %s" % matched_narrate_location)