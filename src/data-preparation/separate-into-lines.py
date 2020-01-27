import os
from os import walk
import re
import nltk
import pandas as pd

class SeparateIntoLines():
    basepath = os.path.dirname(os.path.abspath(__file__))
    datapath = basepath +'/data/hugh-murray/chapter3/chapter3-sections/'  # Datapath for Statement by Members

    newdir_path = basepath
    new_data = pd.DataFrame(columns=['chapterNo', 'chapterTitle', 'sectionNo', 'sectionTitle', 'sentence'])

    def __init__(self):
        super().__init__()
        for root, dirs, files in walk(self.datapath):
            for file in files:
                if file.endswith(".txt"):
                    self.readfile = file
                    self.convert_into_lines(self.datapath, self.readfile,self.new_data)

    def split_into_sentences(self, text):
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

    def convert_into_lines(self, path, file,new_data):

            textfile = open(path+file, "r+")
            fulltext = textfile.read()
            splitted_text = self.split_into_sentences(fulltext)

            titledetails = file.split('.', 1)[0]
            titleno = titledetails.split('-', 1)[0]
            titlename = titledetails.split('-', 1)[1]

            new_row = {}

            for line in splitted_text:
                #print(line)
                new_row['chapterNo'] = 3
                new_row['chapterTitle'] = 'PART 1'
                new_row['sectionNo'] = titleno
                new_row['sectionTitle'] = titlename
                new_row['sentence'] = line
                new_data.loc[len(new_data)] = new_row

            new_data.to_csv(path + 'chapter3.csv',sep='\t', encoding='utf-8', index=False)

    def find_intermediate_chars(self,text, sub1, sub2):
        start = text.index(sub1) + len(sub1)
        end = text.index(sub2)
        return text[start:end]

    def nltk_splitting(self, text):
        sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        splitted_text = sent_detector.tokenize(text.strip())
        return splitted_text

if __name__ == '__main__':
    SeparateIntoLines()
