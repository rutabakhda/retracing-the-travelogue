from pathlib import Path
import pandas as pd
import os
from collections import Counter

datapath = Path(__file__).resolve().parents[2]

def gazetteer_allenNLP(data,data1):
    count = 0
    notgazetteer_location_list = []
    notgazetteer_person_list = []
    allenNLP_location_list = []
    allenNLP_person_list = []

    for index,row in data.iterrows():
        print(index)
        sentence = row['sentence']
        person = row['Person']
        location = row['Location']
        gazetteer_person = row['Gazzeter Person']
        gazetteer_location = row['Gazzeter Location']

        person_list = []
        location_list = []
        gazetteer_person_list = []
        gazetteer_location_list = []

        if not isinstance(person,float):
            person_list = person.split(",")
        if not isinstance(location, float):
            location_list = location.split(",")
        if not isinstance(gazetteer_person, float):
            gazetteer_person_list = gazetteer_person.split(",")
        if not isinstance(gazetteer_location, float):
            gazetteer_location_list = gazetteer_location.split(",")

        person_list = [item.strip() for item in person_list]
        location_list = [item.strip() for item in location_list]
        gazetteer_person_list = [item.strip() for item in gazetteer_person_list]
        gazetteer_location_list = [item.strip() for item in gazetteer_location_list]

        common_person = sorted(list((Counter(person_list) & Counter(gazetteer_person_list)).elements()))
        common_location = sorted(list((Counter(location_list) & Counter(gazetteer_location_list)).elements()))

        notgazetteer_person_li = list((Counter(person_list) - Counter(common_person)).elements())
        notgazetteer_location_li = list((Counter(location_list) - Counter(common_location)).elements())

        notgazetteer_person = ','.join([str(elem) for elem in notgazetteer_person_li])
        notgazetteer_location = ','.join([str(elem) for elem in notgazetteer_location_li])

        allenNLP = data1.iloc[index]
        allenNLP_person = allenNLP['allenNLP Person']
        allenNLP_location= allenNLP['allenNLP Location']

        notgazetteer_location_list.append(notgazetteer_location)
        notgazetteer_person_list.append(notgazetteer_person)
        allenNLP_location_list.append(allenNLP_location)
        allenNLP_person_list.append(allenNLP_person)

        count = count + 1
        print(count)

    data['allenNLP Location'] = allenNLP_location_list
    data['allenNLP Person'] = allenNLP_person_list
    data['notgazetteer Location'] = notgazetteer_location_list
    data['notgazetteer Person'] = notgazetteer_person_list

    return data

book = ['part1','part2','part3']
#book = ['part1']

for part in book:

    readfile = datapath / 'results/hugh-murray/{}/ner/gazetteer-murray-yule-special-index.csv'.format(part)
    data = pd.read_csv(readfile, sep='\t', encoding='latin1', error_bad_lines=False)

    readfile = datapath / 'results/hugh-murray/{}/ner/allenNLP.csv'.format(part)
    data1 = pd.read_csv(readfile, sep='\t', encoding='latin1', error_bad_lines=False)

    outdata = gazetteer_allenNLP(data,data1)

    if not os.path.exists(datapath / 'results/hugh-murray/{}/ner'.format(part)):
       os.makedirs(datapath / 'results/hugh-murray/{}/ner'.format(part))

    writefile = datapath / 'results/hugh-murray/{}/ner/gazetteer-allenNLP.csv'.format(part)
    if os.path.exists(writefile):
        os.remove(writefile)

    outdata.to_csv(writefile, sep='\t', encoding='latin1',index=False)