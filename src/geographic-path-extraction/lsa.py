import pandas as pd
from pathlib import Path
import os
from stanfordcorenlp import StanfordCoreNLP

nlp = StanfordCoreNLP('/home/ruta/master-thesis/tools/stanford-corenlp-full-2018-10-05')
datapath = Path(__file__).resolve().parents[2]
book = ['part1']

for part in book:
	rows_to_keep = [0,525]
	readfile = datapath / 'results/hugh-murray/{}/processed/{}-annotated-special.csv'.format(part, part)
	data = pd.read_csv(readfile, sep='\t', encoding='latin1', error_bad_lines=False,nrows=500)
	#data = pd.read_csv(readfile, sep='\t', encoding='latin1', error_bad_lines=False,skiprows = lambda x: x not in rows_to_keep)
    
	for index,row in data.iterrows():
		sentence = row['sentence']
		location = row['Location']
		result = row['Result']
		
		
		if not isinstance(location,float):
			print(sentence)
			location_list = location.split(",")
			pos_list = nlp.pos_tag(sentence)
			for location_item in location_list:
				
				for item in pos_list:
					if item[0] == location_item:
						print(item[0])
						print(item[1])
						print()
		print("===========================")
		


	
