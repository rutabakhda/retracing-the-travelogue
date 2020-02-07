#!/usr/bin/venv python3
from pathlib import Path
import os
from os import walk
import re
import nltk
import pandas as pd

datapath = Path(__file__).resolve().parents[2]


def split_into_sentences(text):
    alphabets = "([A-Za-z])"
    prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
    suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
    acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
    websites = "[.](com|net|org|io|gov)"
    digits = "([0-9])"

    text = " " + text + "  "
    text = text.replace("\n", " ")
    text = re.sub(prefixes, "\\1<prd>", text)
    text = re.sub(digits + "[.]" + digits, "\\1<prd>\\2", text)
    text = re.sub(websites, "<prd>\\1", text)
    if "Ph.D" in text: text = text.replace("Ph.D.", "Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] ", " \\1<prd> ", text)
    text = re.sub(acronyms + " " + starters, "\\1<stop> \\2", text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]", "\\1<prd>\\2<prd>\\3<prd>", text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]", "\\1<prd>\\2<prd>", text)
    text = re.sub(" " + suffixes + "[.] " + starters, " \\1<stop> \\2", text)
    text = re.sub(" " + suffixes + "[.]", " \\1<prd>", text)
    text = re.sub(" " + alphabets + "[.]", " \\1<prd>", text)
    if "..." in text: text = text.replace("...", "<prd><prd><prd>")
    if "”" in text: text = text.replace(".”", "”.")
    if "\"" in text: text = text.replace(".\"", "\".")
    if "!" in text: text = text.replace("!\"", "\"!")
    if "?" in text: text = text.replace("?\"", "\"?")
    text = text.replace(".", ".<stop>")
    text = text.replace("?", "?<stop>")
    text = text.replace("!", "!<stop>")
    text = text.replace("<prd>", ".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences

def convert_into_lines(file,new_data,part,sentence_counter):

        textfile = open(datapath / 'results/hugh-murray/{}/OCR/{}-sections/'.format(part,part)/file, "r+")
        fulltext = textfile.read()
        splitted_text = split_into_sentences(fulltext)


        titledetails = file.split('.', 1)[0]
        titleno = titledetails.split('-', 1)[0]
        titlename = titledetails.split('-', 1)[1]
        #print(file)
        #print(titleno)
        #print(titlename)
        #print("==========================")
        new_row = {}

        for line in splitted_text:
            sentence_counter = sentence_counter + 1
            #print("{} section".format(titleno))
            #print(line)
            new_row['chapter No'] = part[-1]
            new_row['chapter Title'] = part
            new_row['section No'] = titleno
            new_row['section Title'] = titlename
            new_row['sentence No'] = sentence_counter
            new_row['sentence'] = line
            new_data.loc[len(new_data)] = new_row

        outfile = datapath / 'results/hugh-murray/{}/processed/{}-original.csv'.format(part,part)
        if os.path.exists(outfile):
            os.remove(outfile)

        new_data.to_csv(outfile,sep='\t', encoding='utf-8', index=False)
        return sentence_counter

def find_intermediate_chars(text, sub1, sub2):
    start = text.index(sub1) + len(sub1)
    end = text.index(sub2)
    return text[start:end]

def nltk_splitting(text):
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    splitted_text = sent_detector.tokenize(text.strip())
    return splitted_text


book = ['part1','part2','part3']
#book = ['part1']
for part in book:
    if not os.path.exists(datapath / 'results/hugh-murray/{}/processed'.format(part)):
        os.makedirs(datapath / 'results/hugh-murray/{}/processed'.format(part))

    readsection = datapath / 'results/hugh-murray/{}/OCR/{}-sections/'.format(part,part)  # Datapath for Statement by Members
    new_data = pd.DataFrame(columns=['chapter No', 'chapter Title', 'section No', 'section Title','sentence No','sentence'])

    sentence_counter = 0

    for root, dirs, files in walk(readsection):
        for file in files:
            if file.endswith(".txt"):
                readfile = file
                sentence_counter = convert_into_lines(readfile,new_data,part,sentence_counter)
    print("{} processing have been completed".format(part))