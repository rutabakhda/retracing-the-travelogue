from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
from nltk import Tree
from nltk.tag import StanfordPOSTagger
import os
import pandas as pd

stanford_dir = "E:\python\standford-nlp\stanford-postagger-2018-10-16"
model_file = stanford_dir+"\models\english-bidirectional-distsim.tagger"
jar_file = stanford_dir+"\stanford-postagger.jar"

st = StanfordNERTagger('data\standford-nlp\stanford-ner-2018-10-16\classifiers\english.all.3class.distsim.crf.ser.gz',
                       'data\standford-nlp\stanford-ner-2018-10-16\stanford-ner.jar', encoding='utf-8')

tagger = StanfordPOSTagger(model_filename=model_file, path_to_jar=jar_file)

def get_continuous_chunks(text, label):

    #tagged_text = tagger.tag(text.split())
    #nouns = [word for word,tag in tagged_text if tag.startswith('NN')]
    #print(nouns)

    tokenized_text = word_tokenize(text)
    classified_text = st.tag(tokenized_text)

    tags = [word for word,tag in classified_text if tag == label]
    return tags


sentence = 'for it is the custom of the Tartars, that until the horn termed naccar is winded the troops do not engage.'

basepath = os.path.dirname(os.path.abspath(__file__))
datapath = basepath +'/data/hugh-murray/chapter1/'
readfile = 'chapter1.csv'


data = pd.read_csv(datapath+readfile,sep=',', encoding='ISO-8859-1',error_bad_lines=False)

location_list = []
person_list = []
organization_list = []

count = 0
for index,row in data.iterrows():
    sentence = row['sentence']
    ner_location = get_continuous_chunks(sentence, 'LOCATION')
    ner_person = get_continuous_chunks(sentence, 'PERSON')
    ner_organization = get_continuous_chunks(sentence, 'ORGANIZATION')

    location = ' '.join([str(elem) for elem in ner_location])
    person = ' '.join([str(elem) for elem in ner_person])
    organization = ' '.join([str(elem) for elem in ner_organization])

    location_list.append(location)
    person_list.append(person)
    organization_list.append(organization)
    count = count + 1
    print(count)


data['Stanford Location'] = location_list
data['Standford Person'] = person_list
data['Stadnford organization'] = organization_list

file_name = 'chapter1-standford.csv'
data.to_csv(datapath+file_name, sep='\t', encoding='ISO-8859-1')
#print(type(data))
#print(type(get_continuous_chunks(sentence, 'LOCATION')))
#print(get_continuous_chunks(sentence, 'PERSON'))
#print(get_continuous_chunks(sentence, 'ORGANIZATION'))


