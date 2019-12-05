import os
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

'''
Each chapter is processed individually
Chapter 1 has total of 81 sections
'''
basepath = os.path.dirname(os.path.abspath(__file__))
datapath = basepath +'/data/henry-yule/index/'  # Datapath for Statement by Members
readfile= 'index-full-original.txt'

textfile = open(datapath + readfile, "r+")
fulltext = textfile.read()


#Chapter 1 has 81 sections so range is from 1 to 82
total_sections = 26
#So it finds the content between 2 section numbers (in roman)
for i in range(1,total_sections+1):
    # To extract the data of section i
    # . added as section titles contain full stop at the end

    startchar = pos_to_char(i-1).upper()
    endchar = pos_to_char(i).upper()
    start = startchar+'.'   # Marks the beginning of section i
    end = endchar+'.'   # Marks the end of section i
    text = ""
    print(start)
    print(end)
    # Extracting the text for ith section marked between start and end
    fulltext = fulltext.split(start, 1)[1]
    text = fulltext.split(end, 1)[0]


    # Section title will be used with section number as file name for ith section
    newtextfile = open(datapath + "index-sections/"+startchar+".txt", "w+")

    # section content will be stored as details
    newtextfile.write(text)
    newtextfile.close()