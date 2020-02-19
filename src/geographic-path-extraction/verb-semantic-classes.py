
import nltk
#from nltk.corpus import verbnet as vn
import re
#nltk.download('verbnet')
#nltk.download('framenet_v17')
#nltk.download('propbank')
#vnet3 = nltk.corpus.util.LazyCorpusLoader('verbnet3', nltk.corpus.reader.verbnet.VerbnetCorpusReader,r'(?!\.).*\.xml')

#print(vnet3.classids('travel'))
# vn_results = vn.classids(lemma='come')
#
# match_found = False
# for item in vn_results:
#     #v = vn.vnclass(item)
#
#     #print(item)
#     x = re.search("51.1|51.4.2",item)
#     if x is not None:
#         match_found = True
#
# print(match_found)

    #print(vn.lemmas(item))
    #print(vn.themroles(item))
    #print([t.attrib['type'] for t in v.findall('THEMROLES/THEMROLE')])


#from nltk.corpus import verbnet as vn
from nltk.corpus import framenet as fn
#from nltk.corpus import propbank as pb


input = "speak"
#
# vn_results = vn.classids(lemma=input)
#
# if not vn_results:
#     print (input + ' not in verbnet.')
# else:
#     print ('verbnet:')
#     print (vn_results)
#
fn_results = fn.frames_by_lemma(input)
print(type(fn_results))
if not fn_results:
    print (input + ' not in framenet.')
else:
    for item in fn_results:
        print(item.name)
        print(item.ID)
        id = item.ID
        if id in (54,61, 57, 690, 7):
            print("Match found")
            print(id)
        #else:
        #    print("NOT MATCH")
        #    print(id)



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