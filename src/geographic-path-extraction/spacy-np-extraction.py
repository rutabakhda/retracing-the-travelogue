from spacy.en import English
nlp = English()
doc = nlp(u'The cat and the dog sleep in the basket near the door.')
for np in doc.noun_chunks:
    print(np.text)