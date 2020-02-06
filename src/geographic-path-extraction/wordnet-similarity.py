#WordNet as thesaurus
from nltk.corpus import wordnet as wn
from itertools import product

print(wn.synsets('return', pos=wn.VERB))
#print("=====================================================")
#print(wn.synsets('arrive', pos=wn.VERB))

def word_similarity(wordx,wordy):
    #wordx, wordy = "proceed", "enter"
    sem1, sem2 = wn.synsets(wordx, pos=wn.VERB), wn.synsets(wordy, pos=wn.VERB)
    maxscore = 0
    for i,j in list(product(*[sem1,sem2])):
      score = i.wup_similarity(j) # Wu-Palmer Similarity
      #print(score)
      if score:
        maxscore = score if maxscore < score else maxscore
      else:
          maxscore = 0

    return maxscore


score = word_similarity("tell","exlpain")
print(score)
