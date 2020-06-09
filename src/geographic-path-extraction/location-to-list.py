import html
import pandas as pd
from pathlib import Path
import json
import os
from collections import Counter
import re

def location_to_list(data):
    count = 0
    travelled_location_list = []

    for index,row in data.iterrows():
        #print(row)
        polo_annotated_location = row['Marco Location']
        
        
        if not isinstance(polo_annotated_location, float): 
            #polo_annotated_location = polo_annotated_location.replace("+AHw-","|")
            #polo_annotated_location = polo_annotated_location.replace("+ACI-","ERR")
            #print(polo_annotated_location ) 
   
            temp_travelled_location_list = polo_annotated_location.split(",")
            #print(temp_travelled_location_list)
            for item in temp_travelled_location_list:
                 item1 = re.sub(r"[\n\t]*", "",item)
                 if len(travelled_location_list) == 0:
                     travelled_location_list.append(item1)
                 elif  travelled_location_list[-1] != item1:
                     travelled_location_list.append(item1) 
            #travelled_location_list = travelled_location_list + temp_travelled_location_list
            #print(temp_travelled_location_list)


    for item in travelled_location_list:
        print(item)
    print("*****************")


    #dict_annotated_locations = dict(travelled_location_list)
    dict_annotated_locations= { i : travelled_location_list[i] for i in range(0, len(travelled_location_list) ) }
    print(dict_annotated_locations)
    print(len(travelled_location_list))
    count = count + 1
    df = pd.DataFrame(dict_annotated_locations.items(), columns=['Count','Annotated Travel']) 
  
    return df


datapath = Path(__file__).resolve().parents[2]
book = ['part2']

for part in book:

    readfile = datapath / 'results/hugh-murray/{}/processed/{}-annotated-special.csv'.format(part,part)
    data = pd.read_csv(readfile, sep='\t', encoding='latin1')

    outdata = location_to_list(data)

    writefile = str(datapath) + '/results/hugh-murray/{}/processed/{}-locations.csv'.format(part,part)
    if os.path.exists(writefile):
        os.remove(writefile)

    outdata.to_csv(writefile, sep='\t', encoding='latin1',index=False)


