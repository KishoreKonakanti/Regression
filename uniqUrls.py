# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 11:44:20 2018

@author: kkonakan
"""

import csv
import pandas as pd

def uniqUrls(fname):
    props = ['url','title','descr','numLinks','kwords','AlexaRank','hostedIn','CSS',
         'JS','size']
    inFile = 'D:/AI/Dataset/%s.csv'%fname
    outFile = 'D:/AI/Dataset/%s_curated.csv'%fname
    csvfile = open(outFile,'w', buffering=1)
    #print('1')
    df = None
    #print(inFile)
    try:
        df = pd.read_csv(inFile)
    except Exception as e:
        print(e)
    
    #print('2')
    
    headers = list(df.columns)
    #print('3')
    #print('Headers:',props)
    wr = csv.DictWriter(csvfile, headers)
   # print('4')
    uniqUrls = df['url'].unique()
    uniqDF = pd.DataFrame(None)
    uniqDF.append(headers)
    print('Number of urls:',len(uniqUrls))
    for url in uniqUrls:
        row = df.loc[(df['url'] == url)].head(1)
        #print(row)
        uniqDF.append(row)
        #wr.writerow(row)
        #wr.writerow('\n')
    return uniqDF

print(uniqUrls('AI'))
    