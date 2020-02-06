
import nltk
nltk.download('verbnet')
nltk.download('framenet_v17')
#nltk.download('propbank')
vnet3 = nltk.corpus.util.LazyCorpusLoader('verbnet3', nltk.corpus.reader.verbnet.VerbnetCorpusReader,r'(?!\.).*\.xml')

print(vnet3.classids('travel'))

from nltk.corpus import verbnet as vn
from nltk.corpus import framenet as fn
#from nltk.corpus import propbank as pb


vn_results = vn.classids(lemma=input)

if not vn_results:
    print (input + ' not in verbnet.')
else:
    print ('verbnet:')
    print (vn_results)

fn_results = fn.frames_by_lemma(input)

if not fn_results:
    print (input + ' not in framenet.')
else:
    print ('framenet:')
    print (fn_results)

#pb_results = []
#try:
#    pb_results = pb.rolesets(input)
#except ValueError:
#    print (input + ' not in propbank.')

# if pb_results:
#     print ('propbank:')
#     print (pb_results)
#
# print(pb.verbs())