# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 11:59:25 2018

@author: kkonakan
"""

import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import numpy as np
import matplotlib.pyplot as plt
import os,re
from nltk.tokenize import word_tokenize


def genwordcloud(df, domain):
    kwords = df['kwords']
    kwords = kwords.dropna()
    
    wordset = set()
    
    sw = STOPWORDS
    print('Reading lines')
    for line in kwords:
        tokens = word_tokenize(line)
        for word in tokens:
            if re.match('[a-zA-Z0-9]{2,}', word):
                wordset.add(word)
    
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
    plt.title('Word Cloud of %s'%domain.upper(),fontsize='xx-large')            
    plt.show()
    return wordset

def dynamical(df):
    cond = (df['JS'] == 1.0)
    jscount = len( df[ cond ] )
    numSites = df.shape[0]
    per = (jscount/numSites) * 100
    print('Percentage of dynamic sites: %d'%per)
    return jscount/numSites

def getHostedIn(df):
    uniqNations = pd.DataFrame(df['hostedIn'].unique(),columns=['hostedIn'])
    
    uniqNations.dropna(inplace=True)
    print(uniqNations)
    print('Shapes:', df.shape, uniqNations.shape)
    nation_dict = {}
    for nation in uniqNations.hostedIn:
        print('Nation: %s'%nation)
        cond1 = (df.hostedIn == nation)
        temp = df[ (cond1) ]
        cnt = len(temp)
        print('%d websites hosted in %s'%(cnt,nation))
        nation_dict[nation] = cnt
    del df
    return nation_dict
        
def kwordAnalysis(dataFrame):
    dlwords = ['deep','learning']
    mlwords = ['machine','automated']
    ai = ['artificial','intelligence','ai']
    general = ['learning']
    kwords = dataFrame['kwords']
    
    kw_dict = {'dl':0,'ml':0,'ai':0,'gen':0,'other':0}
    
    kwords = dataFrame['kwords']
    kwords = kwords.dropna()
    
    kwordset = set()
    
    sw = STOPWORDS
    print('Reading lines')
    for line in kwords:
        tokens = word_tokenize(line)
        for word in tokens:
            if re.match('[a-zA-Z0-9]{2,}', word):
                kwordset.add(word)
    
    kwordset = kwordset.difference(sw)

    for word in kwordset:
        if word in dlwords:
            kw_dict['dl'] += 1
        elif word in mlwords:
            kw_dict['ml'] += 1
        elif word in ai:
            kw_dict['ai'] += 1
        elif word in general:
            kw_dict['gen'] += 1
        else:
            kw_dict['other'] += 1
            
    print(kw_dict)
    return kw_dict

def comparison(ai,io):
    arai = ai.AlexaRank
    ario = io.AlexaRank
    arai = np.array(arai[:543], dtype=int)
    ario = np.array(ario[:543], dtype=int)
    r = np.arange(0,543)
    plt.scatter(arai,r,label='AI')
    plt.scatter(ario,r, label='IO')
    plt.legend(loc='upper right')
    plt.figure(figsize=(10,10))
    plt.show()

# Load data
DOMAIN_LIST=['IO','AI','ML']
DOMAIN_LIST=['AI']
for domain in DOMAIN_LIST:
    dataFile = 'D:/AI/Dataset/%s.csv'%domain
    if os.path.isfile(dataFile):
        print('DOMAIN: ', domain)
        data = pd.read_csv(dataFile,encoding='utf-8-sig')
        print(data.shape)
        #keywordset = genwordcloud(data, domain)
        dynamical(data)
        nat_dict = getHostedIn(data.copy())
        kw_dict = kwordAnalysis(data)