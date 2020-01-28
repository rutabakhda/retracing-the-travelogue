from pprint import pprint
from pycorenlp.corenlp import StanfordCoreNLP
host = "http://localhost"
port = "9000"
nlp = StanfordCoreNLP(host + ":" + port)
text = "Joshua Brown, 40, was killed in Florida in May when his Tesla failed to " \
       "differentiate between the side of a turning truck and the sky while " \
       "operating in autopilot mode."
output = nlp.annotate(
    text,
    properties={
        "outputFormat": "json",
        "annotators": "depparse,ner,entitymentions,sentiment"
    }
)
pprint(output)