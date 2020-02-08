#!/usr/bin/venv python3
"""
    Converts Index file by yule in csv after formatting.

    For each entity name in index, there are multiple mentions. Example is,
    Abyssinia (Abash),
        its king’s punishment of Soldan of Aden;
        dominion on the coast, mediaeval history and chronology;
        table of kings;
        wars with Mahomedan states.

    This code separates that into separate lines with each line containing
    entity name and its meaning.
"""

from pathlib import Path
import os
import re
import string
import pandas as pd


def text_to_csv(textfile, csvfile):

    new_data = pd.DataFrame(columns=['Entity Name', 'Type'])

    with open(textfile,encoding="utf-8-sig") as fp:
        line = fp.readline()
        cnt = 1
        while line:
            # Entity could be with mention or without mention.
            # Entity with mention could be single line or multiple lines.
            # For each line, we need to check

            new_row = {}
            # It checks if it doesn't ends with full stop.
            if re.match('^[A-Z][^?!.]*[.]$', line) is None:
                # If it begins with capital letter then it's the beginning of new entity but with multiple mentions.
                if line[0].isupper():
                    # If it has mention, entity and mention are separated by comma.
                    # case 1 : Beginning of entity with mention. Example - Aijaruc, Kaidu’s daughter,
                    if ',' in line:
                        title = line.split(',', 1)[0]
                        content = line.split(',', 1)[1]
                    # case 2 : Beginning of new entity without mention. Example - Acomat Soldan (Ahmad Sultan),
                    else:
                        title = line
                        content = ""
                # Begins with small letter so continuation of current entity with another mention.
                else:
                    content = line
            # If it ends with full stop.
            else:
                # case 1 : Entity with single mention. Example - Adamodana, Castle of.
                if ',' in line:
                    title = line.split(',', 1)[0]
                    content = line.split(',', 1)[1]
                # case 2 : Just entity name without mention. Example - Aepyornis and its eggs.
                else:
                    title = line
                    content = ""

            title = title.strip()
            content = content.strip()

            if content and content[-1] in string.punctuation:
                content = content[:-1]

            if title and title[-1] in string.punctuation:
                title = title[:-1]

            new_row['Entity Name'] = title
            new_row['Type'] = content
            new_data.loc[len(new_data)] = new_row
            print("title = " + str(title))
            print('content = {0}'.format(str(content)))
            line = fp.readline()
        new_data.to_csv(csvfile, sep="\t",encoding='utf-8-sig', index=False)


part = "index"
datapath = Path(__file__).resolve().parents[2]
index_path = datapath / 'data/henry-yule/{}/'.format(part)

if not os.path.exists(datapath / 'results/henry-yule/{}/processed'.format(part)):
    os.makedirs(datapath / 'results/henry-yule/{}/processed'.format(part))

textfile = datapath / 'results/henry-yule/{}/OCR/{}-yule-fulltext.txt'.format(part,part) # Input text file of Index
csvfile = datapath / 'results/henry-yule/{}/processed/{}-original.csv'.format(part,part) # Output csv file for Index
text_to_csv(textfile,csvfile)