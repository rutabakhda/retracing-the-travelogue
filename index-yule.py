from pathlib import Path
import os
import re
import string
import pandas as pd

index_path = os.path.dirname(os.path.abspath(__file__)) + '/data/henry-yule/index/'

print(index_path)

file_path = index_path + '/index-yule.txt'
new_data = pd.DataFrame(columns=['Entity Name', 'Type'])
with open(file_path,encoding="utf-8-sig") as fp:
    line = fp.readline()
    cnt = 1
    while line:
        new_row = {}
        if re.match('^[A-Z][^?!.]*[.]$', line) is None:
            if line[0].isupper():
                if ',' in line:
                    title = line.split(',', 1)[0]
                    content = line.split(',', 1)[1]
                else:
                    title = line
                    content = ""

            else:
                #title = line.split(',', 1)[0]
                content = line
        else:
            if ',' in line:
                title = line.split(',', 1)[0]
                content = line.split(',', 1)[1]
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
        print("content = " + str(content))
        line = fp.readline()
    new_data.to_csv(index_path + 'index.csv', encoding='utf-8-sig', index=False)