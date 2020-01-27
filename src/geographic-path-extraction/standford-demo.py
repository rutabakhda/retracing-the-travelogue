import stanfordnlp
stanfordnlp.download('en')

nlp = stanfordnlp.Pipeline()
doc = nlp("Having described so many inland provinces, I will now enter upon India, with the wonderful objects in that region.")
doc.sentences[0].print_dependencies()