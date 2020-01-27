# from pathlib import Path
# # Simple usage
# from stanfordcorenlp import StanfordCoreNLP
#
# datapath = Path(__file__).resolve().parent.parent.parent
#
# print(datapath / 'tools/stanford-corenlp-full-2018-10-05')
# print("==================================================================")
# nlp = StanfordCoreNLP('/home/newo1347/PycharmProjects/ruta-thesis/tools/stanford-corenlp-full-2018-10-05')
#
# sentence = 'Guangdong University of Foreign Studies is located in Guangzhou.'
# print ('Tokenize:', nlp.word_tokenize(sentence))
# print ('Part of Speech:', nlp.pos_tag(sentence))
# print ('Named Entities:', nlp.ner(sentence))
# print ('Constituency Parsing:', nlp.parse(sentence))
# print ('Dependency Parsing:', nlp.dependency_parse(sentence))

#nlp.close() # Do not forget to close! The backend server will consume a lot memery.

from stanfordcorenlp import StanfordCoreNLP
from nltk.tree import Tree
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from itertools import product
import pandas as pd
from pathlib import Path

nlp = StanfordCoreNLP('/home/newo1347/PycharmProjects/ruta-thesis/tools/stanford-corenlp-full-2018-10-05')

sentence = 'and first, of one named Zipangu.'

def extract_phrase(tree_str, label):
    phrases = []
    trees = Tree.fromstring(tree_str)
    for tree in trees:
        for subtree in tree.subtrees():
            if subtree.label() == label:
                t = subtree
                t = ' '.join(t.leaves())
                phrases.append(t)

    return phrases

def word_similarity(wordx,wordy):
    #wordx, wordy = "proceed", "enter"
    sem1, sem2 = wn.synsets(wordx), wn.synsets(wordy)
    maxscore = 0
    for i,j in list(product(*[sem1,sem2])):
      score = i.wup_similarity(j) # Wu-Palmer Similarity
      #print(score)
      if score:
        maxscore = score if maxscore < score else maxscore
      else:
          maxscore = 0

    return maxscore

datapath = Path(__file__).resolve().parents[2]

# Input individual index files
readfile = datapath / 'data/hugh-murray/chapter3/chapter3.csv'

data = pd.read_csv(readfile,sep=',', encoding='latin1',error_bad_lines=False)
count = 0
narrate_final_list = []
narrate_flag_list = []
travel_final_list = []
travel_flag_list = []

for index,row in data.iterrows():
    sentence = row['sentence']
    pos = nlp.pos_tag(sentence)
    #print(pos)

    verbs = [item[0] for item in pos if item[1] in {'VB','VBD','VBG','VBN'}]
    #print(verbs)
    base_verb = [WordNetLemmatizer().lemmatize(word,'v') for word in verbs]
    #print(base_verb)

    narrate_list = ['describe','narrate']
    travel_list = ['travel','voyage']

    narrate_flag = 0
    travel_flag = 0
    score_narrate = 0
    score_travel = 0

    narrate = []
    travel = []

    for verb in base_verb:
        #print("verb is %s =" % verb)
        for item in narrate_list:
            #print(item)
            score_narrate = word_similarity(verb,item)
            #print(score_narrate)
            if score_narrate > 0.5:
              narrate_flag = 1
              narrate.append(verb)
              break

        for item in travel_list:
            #print(item)
            score_travel = word_similarity(verb,item)
            #print(score_travel)
            if score_travel > 0.5:
              travel_flag = 1
              travel.append(verb)
              break

    narrate_str = ','.join([str(elem) for elem in narrate])
    travel_str = ','.join([str(elem) for elem in travel])

    narrate_flag_list.append(narrate_flag)
    narrate_final_list.append(narrate_str)
    travel_flag_list.append(travel_flag)
    travel_final_list.append(travel_str)

    count = count + 1
    print(count)

data['Is Narrate'] = narrate_flag_list
data['Is Travel'] = travel_flag_list
data['Narrate Verbs'] = narrate_final_list
data['Travel Verbs'] = travel_final_list

writefile = datapath / 'data/hugh-murray/chapter3/chapter3-find-travel.csv'

data.to_csv(writefile, sep='\t', encoding='latin1')


nlp.close()

#tree_str = nlp.parse(sentence)
#print (tree_str)
# u'(ROOT\n  (SBARQ\n    (WHNP (WP Who))\n    (SQ\n      (VP (VBZ drives)\n        (NP (DT a) (NN tractor))))\n    (. ?)))'

#nps = extract_phrase(tree_str, 'NP')
#print (nps)
#print("=====================================================")
#vps = extract_phrase(tree_str, 'VP')
#print (vps)
#print("=====================================================")
#print ('Part of Speech:', nlp.pos_tag(sentence))
#print("=====================================================")
#print ('Dependency Parsing:', nlp.dependency_parse(sentence))
#print("=====================================================")
#print ('Constituency Parsing:', nlp.parse(sentence))




