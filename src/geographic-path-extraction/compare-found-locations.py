import pandas as pd
from pathlib import Path
import json
import os
from collections import Counter
import re

def Convert(string):
    """

    :param string: Input string
    :return: list from the string
    """
    li = list(string.split(","))
    #print(li)
    return li

def compare(data,data_algo):
	
	new_list = []
	count_list = []
	count = 0
	str1 = data["Annotated Travel"].str.cat(sep=',')
	str2 = data_algo["Annotated Travel"].str.cat(sep=',')
    
	convert_list_of_str1 = (Convert(str1))
	convert_list_of_str2 = (Convert(str2))
  
	list_of_str1 = [item.strip() for item in convert_list_of_str1]
	list_of_str2 = [item.strip() for item in convert_list_of_str2]
	
	print(list_of_str1)
	print(list_of_str2)
	
	for item in list_of_str1:
		print(item)
		if item in list_of_str2:
			print("yes")
			new_list.append(item)
		else:
			print("no")
			new_list.append("")
	
		count = count + 1
		count_list.append(count)
		   
		print("")
	print(new_list)
	
	df = pd.DataFrame(list(zip(count_list,list_of_str1,new_list)),columns=['Count','Annotated Travelled Locations','Found Travelled Locations'])
	return df
	
	
datapath = Path(__file__).resolve().parents[2]
book = ['part1']

for part in book:

	readfile = datapath / 'results/hugh-murray/{}/processed/{}-locations.csv'.format(part,part)
	data = pd.read_csv(readfile, sep='\t', encoding='latin1')

	readfile_algo = str(datapath) + '/results/hugh-murray/{}/geograhpic-path-extraction/{}-locations-voted-annotated.csv'.format(part,part)
	data_algo = pd.read_csv(readfile_algo, sep='\t', encoding='latin1')

    #print(data)
    #print(data_algo)
    
	outdata = compare(data,data_algo)
	writefile = str(datapath) + '/results/hugh-murray/{}/geograhpic-path-extraction/{}-location-comparision-voted-annotated.csv'.format(part, part)

	if os.path.exists(writefile):
		os.remove(writefile)
	
	outdata.to_csv(writefile, sep='\t', encoding='latin1', index=False)
