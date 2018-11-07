# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 11:59:25 2018

@author: kkonakan
"""

import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import numpy as np
import matplotlib.pyplot as plt
import os
from nltk.tokenize import word_tokenize


def genwordcloud(df):
    kwords = df['kwords']
    kwords = kwords.dropna()
    
    wordset = set()
    
    sw = STOPWORDS
    print('Reading lines')
    for line in kwords:
        tokens = word_tokenize(line)
        [wordset.add(word) for word in tokens]
    
    wordset = wordset.difference(sw)

    if wordset is None:
        return None
    kwstr = ''
    for word in wordset:
        kwstr = kwstr + ' ' + word

    print('Number of key words:', len(wordset))
    print('Length of the string:', len(kwstr))

    wordcloud = WordCloud(width=800, height=800, background_color='white', stopwords=sw, min_font_size=10).generate(kwstr)
    plt.figure(figsize=(10, 10))
    plt.imshow(wordcloud)
    plt.show()

def dynamical(df):
    jscount = len( df[ (df['JS'] == '1') ] )
    numSites = df.shape[0]
    per = (jscount/numSites) * 100
    print('%d of dynamic sites'%per)
    return jscount/numSites

def kwordAnalysis(dataFrame):
    

def processData(dataframe):
    pass

# Load data
DOMAIN_LIST=['IO','AI','ML']
for domain in DOMAIN_LIST:
    dataFile = 'D:/AI/Dataset/%s.csv'%domain
    if os.path.isfile(dataFile):
        print('DOMAIN: ', domain)
        data = pd.read_csv(dataFile,encoding='utf-8-sig')
        print(data.shape)
        #genwordcloud(data)
        dynamical(data)