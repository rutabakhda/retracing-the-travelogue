import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()


doc = nlp('kingdom of')
print([(X.text, X.label_) for X in doc.ents])