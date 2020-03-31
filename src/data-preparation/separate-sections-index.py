#!/usr/bin/venv python3
import os
from pathlib import Path
'''
Finding and storing sections of each chapter into separate text files
each text file contains the number and title of each section
https://www.w3resource.com/python-exercises/class-exercises/python-class-exercise-1.php
'''
def char_position(letter):
    return ord(letter) - 97

def pos_to_char(pos):
    return chr(pos + 97)
'''
Finds the text between 2 given strings
'''
def find_intermediate_chars(text, sub1, sub2):
    start = text.index(sub1) + len(sub1)
    end = text.index(sub2)
    return text[start:end]


def separate_section(readfile,total_sections,part):
    textfile = open(readfile, "r+")
    fulltext = textfile.read()

    #So it finds the content between 2 section numbers (in roman)
    for i in range(1,total_sections+1):
        # To extract the data of section i
        # . added as section titles contain full stop at the end

        startchar = pos_to_char(i-1).upper()
        endchar = pos_to_char(i).upper()
        start = startchar+'.'   # Marks the beginning of section i
        end = endchar+'.'   # Marks the end of section i
        text = ""
        # Extracting the text for ith section marked between start and end
        fulltext = fulltext.split(start, 1)[1]
        text = fulltext.split(end, 1)[0]

        if not os.path.exists(datapath / 'results/hugh-murray/{}/OCR/{}-sections'.format(part, part)):
            os.makedirs(datapath / 'results/hugh-murray/{}/OCR/{}-sections'.format(part, part))

        # Section title will be used with section number as file name for ith section
        newtextfile = open(datapath / 'results/hugh-murray/{}/OCR/{}-sections/{}.txt'.format(part, part,startchar),"w+")

        # section content will be stored as details
        newtextfile.write(text)
        newtextfile.close()

    print("{} sections had been generated".format(part))

'''
Each chapter is processed individually
Chapter 1 has total of 81 sections
'''
# Path of the scanned pdf
datapath = Path(__file__).resolve().parents[2]
#book = ['part1','part2','part3']
part = "index"
readfile = datapath / 'results/hugh-murray/{}/OCR/{}-full-corrected.txt'.format(part, part)
total_sections = 26
separate_section(readfile,total_sections,part)
