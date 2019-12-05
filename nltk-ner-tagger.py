import os
import nltk
from nltk import pos_tag,word_tokenize
from nltk.chunk import conlltags2tree, tree2conlltags
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk import Tree
import pandas as pd

def get_continuous_chunks(sentence, label):
    tagged_text = ne_chunk(pos_tag(word_tokenize(sentence)))
    #print(tagged_text)
    #nouns = [word for word, tag in tagged_text if tag.startswith('NN')]
    #print(nouns)

    prev = None
    continuous_chunk = []
    current_chunk = []

    for subtree in tagged_text:
        if type(subtree) == Tree and subtree.label() == label:
            current_chunk.append(" ".join([token for token, pos in subtree.leaves()]))
        elif current_chunk:
            named_entity = " ".join(current_chunk)
            if named_entity not in continuous_chunk:
                continuous_chunk.append(named_entity)
                current_chunk = []
        else:
            continue

    return continuous_chunk


basepath = os.path.dirname(os.path.abspath(__file__))
datapath = basepath +'/data/hugh-murray/chapter1/'
readfile = 'chapter1.csv'


data = pd.read_csv(datapath+readfile,sep=',', encoding='ISO-8859-1',error_bad_lines=False,nrows=100)

location_list = []
person_list = []
organization_list = []

count = 0
for index,row in data.iterrows():
    sentence = row['sentence']
    ner_location = get_continuous_chunks(sentence, 'GPE')
    ner_person = get_continuous_chunks(sentence, 'PERSON')
    ner_organization = get_continuous_chunks(sentence, 'ORGANIZATION')

    location = ', '.join([str(elem) for elem in ner_location])
    person = ' ,'.join([str(elem) for elem in ner_person])
    organization = ' ,'.join([str(elem) for elem in ner_organization])


    location_list.append(location)
    person_list.append(person)
    organization_list.append(organization)
    count = count + 1
    print(count)


data['NLTK Location'] = location_list
data['NLTK Person'] = person_list
data['NLTK organization'] = organization_list

file_name = 'chapter1-nltk.csv'
data.to_csv(datapath+file_name, sep='\t', encoding='ISO-8859-1')






