#!/usr/bin/venv python3
import os
from pathlib import Path
'''
Finding and storing sections of each chapter into separate text files
each text file contains the number and title of each section
https://www.w3resource.com/python-exercises/class-exercises/python-class-exercise-1.php
'''

'''
Converts integer number to roman numbers as section numbers are given in roman numbers
'''
def int_to_Roman(num):
    val = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
    ]
    syb = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV",
        "I"
    ]
    roman_num = ''
    i = 0
    while num > 0:
        for _ in range(num // val[i]):
            roman_num += syb[i]
            num -= val[i]
        i += 1
    return roman_num
'''
Finds the text between 2 given strings
'''
def find_intermediate_chars(text, sub1, sub2):
    start = text.index(sub1) + len(sub1)
    end = text.index(sub2)
    return text[start:end]

'''
Each chapter is processed individually
Chapter 1 has total of 81 sections
'''
# Path of the scanned pdf
datapath = Path(__file__).resolve().parents[2]
#book = ['part1','part2','part3']
part = "part3"
readfile = datapath / 'results/hugh-murray/{}/OCR/{}-full-corrected.txt'.format(part, part)

textfile = open(readfile, "r+")
fulltext = textfile.read()


#Chapter 1 has 81 sections so range is from 1 to 82
total_sections = 61

if not os.path.exists(datapath / 'results/hugh-murray/{}/OCR/{}-sections'.format(part, part)):
    os.makedirs(datapath / 'results/hugh-murray/{}/OCR/{}-sections'.format(part, part))

#So it finds the content between 2 section numbers (in roman)
for i in range(1,total_sections+1):
    # To extract the data of section i
    # . added as section titles contain full stop at the end

    start = int_to_Roman(i)+'.'   # Marks the beginning of section i
    end = int_to_Roman(i+1)+'.'   # Marks the end of section i
    text = ""
    #print(start)
    #print(end)
    # Extracting the text for ith section marked between start and end
    fulltext = fulltext.split(start, 1)[1]
    text = fulltext.split(end, 1)[0]
    text = text.replace("\n"," ")

    # Section content has title and content both so it separates title and content
    title = text.split('.', 1)[0]
    title = title[1:].strip()
    content = text.split('.', 1)[1].strip()

    # Section title will be used with section number as file name for ith section
    newtextfile = open(datapath / 'results/hugh-murray/{}/OCR/{}-sections/{}-{}.txt'.format(part, part,i,title), "w+")

    # section content will be stored as details
    newtextfile.write(content)
    newtextfile.close()