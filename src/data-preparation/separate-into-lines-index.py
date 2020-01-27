import os
from os import walk
import re
import nltk
import pandas as pd
import numpy as np
import string

class SeparateIntoLines():
    basepath = os.path.dirname(os.path.abspath(__file__))
    datapath = basepath +'/data/henry-yule/index/index-sections/'  # Datapath for Statement by Members

    newdir_path = basepath
    new_data = pd.DataFrame(columns=['Entity Name', 'Type', 'Page No'])

    def __init__(self):
        super().__init__()
        for root, dirs, files in walk(self.datapath):
            for file in files:
                if file.endswith(".txt"):
                    print("file name")
                    print(file)
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

            textfile = open(path+file, "r+",encoding='utf-8-sig')
            fulltext = textfile.readlines()
            #fulltext = ' '.join(fulltext)

            #a = fulltext.rsplit('.')[1]

            #fulltext = fulltext.strip()
            #finaltext =  fulltext.replace(a,'')
            print("---------------final text------------------")
            #print(fulltext)
            print("========")
            new_row = {}
            if (len(fulltext)!=0) :
                c = 0
                for line in fulltext:
                    c = c + 1
                    print(c)
                    print(line)
                    title = line.split(',', 1)[0]
                    content = line.split(',', 1)[1]
                    subsections = self.split_into_sentences(content)

                    for section in subsections:

                        if(section[0].isdigit()):

                            section_content = ""
                            pageno = section.strip()
                        else:

                            split_section = re.split(r'(^[^\d]+)', section)[1:]
                            section_content = split_section[0].strip()
                            pageno = split_section[1].strip()

                        if section_content and  section_content[-1] in string.punctuation:
                                section_content = section_content[:-1]

                        if pageno and pageno[-1] in string.punctuation:
                                pageno = pageno[:-1]

                        new_row['Entity Name'] = title
                        new_row['Type'] = section_content
                        new_row['Page No'] = pageno
                        new_data.loc[len(new_data)] = new_row
            new_data.to_csv(path + 'index.csv', encoding='utf-8', index=False)

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
