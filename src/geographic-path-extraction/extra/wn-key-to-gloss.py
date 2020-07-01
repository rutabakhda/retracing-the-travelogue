import re
from nltk.corpus import wordnet as wn

sense_key_regex = r"(.*)\%(.*):(.*):(.*):(.*):(.*)"
synset_types = {1:'n', 2:'v', 3:'a', 4:'r', 5:'s'}

def synset_from_sense_key(sense_key):
    lemma, ss_type, lex_num, lex_id, head_word, head_id = re.match(sense_key_regex, sense_key).groups()
    ss_idx = '.'.join([lemma, synset_types[int(ss_type)], lex_id])
    return wn.synset(ss_idx)

#x = "visit%2:38:00::"
#y = "visit%2:41:02::"

#x = "come%2:38:04::"
#y = "come%2:30:01::"

#x = "quit%2:38:00::"
x = "steal%2:38:01::"
#print(synset_from_sense_key(x))
#print(synset_from_sense_key(y))
ls = []
syn= wn.synsets("quit", pos=wn.VERB)
print(syn)
for item in syn:
	print(item)
	ls = ls + wn.synset(item.name()).lemma_names()
	print(wn.synset(item.name()).lemma_names())

print()
print(ls)
print("=============================")
#print(wn.synset("embark.v.02").lemma_names())
#eat = wn.lemma('arrive.v.01.arrive')
#print(eat.key())
#print(wn.synset("come.v.04").lemma_names())
