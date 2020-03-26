from nltk.stem.wordnet import WordNetLemmatizer
from pathlib import Path
import pandas as pd
import os
import nltk
import re
from nltk.corpus import framenet as fn
from stanfordcorenlp import StanfordCoreNLP

#nltk.download("framenet_v17")

datapath = Path(__file__).resolve().parents[2]
nlp = StanfordCoreNLP('/home/ruta/master-thesis/tools/stanford-corenlp-full-2018-10-05')


def find_frames(word):
    frames_list = []
    fn_results = fn.frames_by_lemma(word)
    for item in fn_results:
        name = item.name
        #print(name)
        frames_list.append(name)
    return frames_list



frames = find_frames("speak")
print(frames)
nlp.close()
