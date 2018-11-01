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
    file = 'D:/AI/Dataset/%s.csv'%fname
    csvfile = open(file,'w')
    print('1')
    df = None
    print(file)
    df = pd.read_csv(file)
    print('2')
    
    headers = list(df.columns)
    print('3')
    print('Headers:',props)
    wr = csv.DictWriter(csvfile, headers)
    print('4')
    uniqUrls = df['url'].unique()
    for url in uniqUrls:
        row = df.loc[(df['url'] == url)].head(1)
        wr.writerow(row)
        wr.writerow('\n')
    return df

df = uniqUrls('AI')
    