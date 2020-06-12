import html
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
    print(li)
    return li


def location_before_after_counts(data):
    count = 0
    before_list = []
    after_list = []
    
    length =  data['Annotated Travel'].count()
    

    for index,row in data.iterrows():

        c = row['Count']
        before = c - 1
        after = length - c
        
        before_list.append(before)
        after_list.append(after)
        
    data['Before Count'] = before_list
    data['After Count'] = after_list
     
        
        
        
    count = count + 1
    #df = pd.DataFrame(dict_annotated_locations.items(), columns=['Count','Annotated Travel']) 
  
    return data
    
def compare_before_after(data,data_algo,data_comparision):
	count = 0
	annotated_before_list = []
	annotated_after_list = []
	algo_before_list = []
	algo_after_list = []
	
	for index,row in data_comparision.iterrows():
		annotated_travel_location = row['Annotated Travelled Locations']
		found_travel_location = row['Found Travelled Locations']
		
		print(annotated_travel_location)
		print(found_travel_location)
		
		
		before_count = ""
		after_count = ""
		algo_before_count = ""
		algo_after_count = ""
			
		data_temp = data.loc[data['Annotated Travel'] == annotated_travel_location]

		for index1,row1 in data_temp.iterrows():
			before_count = row1['Before Count']
			after_count = row1['After Count']
		
		
		if not isinstance(found_travel_location,float):
			print("COMES HERE")
			data_algo_temp = data_algo.loc[data_algo['Annotated Travel'] == found_travel_location]
			print(data_algo_temp)
			for index2,row2 in data_algo_temp.iterrows():
				algo_before_count = row2['Before Count']
				algo_after_count = row2['After Count']
				
		print(before_count)
		print(after_count)
		print(algo_before_count)
		print(algo_after_count)
				
		annotated_before_list.append(before_count)
		annotated_after_list.append(after_count)
		algo_before_list.append(algo_before_count)
		algo_after_list.append(algo_after_count)
			
		count = count + 1
		#print(count)
		print("========================")	    

	data_comparision['Before Count Annotated Location'] = annotated_before_list
	data_comparision['Before Count Found Location'] = algo_before_list
	data_comparision['After Count Annotated Location'] = annotated_after_list
	data_comparision['After Count Found Location'] = algo_after_list

	return data_comparision


datapath = Path(__file__).resolve().parents[2]
book = ['part1']

#for part in book:

#   readfile = datapath / 'results/hugh-murray/{}/processed/{}-locations.csv'.format(part,part)
#    data = pd.read_csv(readfile, sep='\t', encoding='latin1')

#    outdata = location_before_after_counts(data)

#    writefile = str(datapath) + '/results/hugh-murray/{}/processed/{}-locations.csv'.format(part,part)
#    if os.path.exists(writefile):
#        os.remove(writefile)

#    outdata.to_csv(writefile, sep='\t', encoding='latin1',index=False)
    
    
    


for part in book:

	readfile = datapath / 'results/hugh-murray/{}/processed/{}-locations.csv'.format(part,part)
	data = pd.read_csv(readfile, sep='\t', encoding='latin1')

	readfile_algo = str(datapath) + '/results/hugh-murray/{}/geograhpic-path-extraction/{}-locations-annotated-annotated.csv'.format(part,part)
	data_algo = pd.read_csv(readfile_algo, sep='\t', encoding='latin1')

	readfile_comparision = str(datapath) + '/results/hugh-murray/{}/geograhpic-path-extraction/{}-location-comparision-annotated-annotated (copy).csv'.format(part, part)
	data_comparision = pd.read_csv(readfile_comparision, sep='\t', encoding='latin1')
	
	outdata = compare_before_after(data,data_algo,data_comparision)

	#outdata = compare(data,data_algo)
	writefile = str(datapath) + '/results/hugh-murray/{}/geograhpic-path-extraction/{}-location-comparision-annotated-annotated.csv'.format(part, part)

	if os.path.exists(writefile):
		os.remove(writefile)
	
	outdata.to_csv(writefile, sep='\t', encoding='latin1', index=False)
