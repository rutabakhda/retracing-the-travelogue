from nltk.corpus import wordnet as wn
from itertools import product
from nltk.stem.wordnet import WordNetLemmatizer
from pathlib import Path
import pandas as pd
import os
import nltk
import re
from nltk.corpus import verbnet as vn
from xml.etree import ElementTree


from stanfordcorenlp import StanfordCoreNLP

datapath = Path(__file__).resolve().parents[2]
nlp = StanfordCoreNLP('/home/ruta/master-thesis/tools/stanford-corenlp-full-2018-10-05')


vn_31_2 = ElementTree.tostring(vn.vnclass('escape-51.1'))

