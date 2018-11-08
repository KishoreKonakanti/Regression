# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 12:56:39 2018

@author: kkonakan
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from langdetect import DetectorFactory
import re
import time
from collections import Counter

DetectorFactory.seed = 0
nonEng = []
EngWords = []

def genwordcloud(wordset,name):
    print('Incoming:',name)
    #print('Incoming:',wordset)
    if wordset is None:
        return None
    kwstr = ''
    for word in wordset:
        kwstr = kwstr + ' ' + word

    wordcloud = WordCloud(width=1000, height=1000, background_color='white', 
                          stopwords=stopwords.words('english'),\
                          min_font_size=10).generate(kwstr)
    title= 'WordCloud for domain:'+name
    plt.figure(figsize=(14, 14))
    plt.imshow(wordcloud)
    plt.title(title.upper())
    plt.show()

def arankAnalysis(df):
    '''
        Steps
            1. Load AlexaRanks
            2. Convert to int using pd.to_numeric
            3. Sort values
            4. Scale data using StandardScaler
            5. Plot data
    '''
    import matplotlib.pyplot as plt
    import sklearn.preprocessing as skp
    
    AR = pd.DataFrame(df.AlexaRank)
    
    intar = AR[ pd.to_numeric(AR['AlexaRank'], errors='coerce').notnull()]
    intar = intar.sort_values('AlexaRank')
    
    ss = skp.StandardScaler()
    scaledar = ss.fit_transform(intar)
    global colors
    
    plt.hist(scaledar, color=colors.pop(),label='AI')
    plt.show()
    
    del plt
    
    return None

def hostedAnalysis(df):
    hin = df.groupby(['hostedIn']).size()
    hin_dict = pd.DataFrame(data=[],columns=['Country', 'Count'])
    loc = 0
    for ind in hin.index:
        country = ind
        count = hin[ind]
        hin_dict.loc[loc] = [country,count]
        loc += 1
    del hin
    
    return hin_dict

def manualAnalysis(wordset):
    aicnt = 0
    mlcnt = 0
    dlcnt = 0
    othcnt = 0
    
    aiwords = ['artificial','artificiallearning', \
               'artificial intelligence','ai','automat',\
               'intelligence','alexa']
    dlwords = ['deep','deep learning','deeplearning','dl']
    mlwords = ['machine','learning', 'machine learning' 'machinelearning','ml']
    Lwords = ['course','education', 'code','coding','coded']
    
    for word in wordset:
        if word in aiwords :
            aicnt += 1
        elif word in mlwords:
            mlcnt += 1
        elif word in dlwords:
            dlcnt += 1
        

def getlangset(wordset):
    import langid as lid
    engwords = set()
    for word in wordset:
        if len(word) > 2:
            lang, conf = lid.classify(word)
            if conf > 0.8:
                engwords.add(word)
        else:
            continue
    return engwords
    '''
    estTime = len(wordset) * 0.3 #(0.1 for sleep and 0.2 for google api call)
    print('Estimated time: %.2f seconds'%estTime)
    from textblob import TextBlob
    langset = set()
    engwords = set()
    otherwords = set()
    for word in wordset:
        lang = TextBlob(word).detect_language()
        langset.add(lang) 
        if (lang == 'en'):
            engwords.add(word)
        else:
            otherwords.add(word)        
        time.sleep(0.1)
    return langset, engwords, otherwords
    '''

def kwordAnalysis(df, name):
    kwords = df.kwords
    kwords.dropna(inplace=True)
    wordset = set()
    sw = stopwords.words('english')
    for line in kwords:
        tokens = word_tokenize(line)
        [wordset.add(word) if len(word)>2 else None for word in tokens]
    if name == 'IO':
       wordset = set()
       for line in df.kwords:
           line = re.subn(' ','', line)[0]
           for word in line.split(','):
               wordset.add(word)
    wordset.difference_update(sw)
    Ewords = getlangset(wordset)
    
    print('Top 10 words with their counts used:',Counter(wordset).most_common(10))
    print('Top 10 english words used:',Counter(Ewords).most_common(10))
   
    #genwordcloud(wordset,name)
    
    return wordset
    del wordset
    
def hostedplot(gh):
    country_list = list(gh.Country)
    total = list(gh.Total)
    y_coords = np.arange(len(gh))
    import matplotlib.pyplot as plt

    plt.figure(figsize=(15,15))
    plt.xscale('symlog')
    plt.ylabel('Countries')
    plt.xlabel('Number of websites hosted')
    sz = list(gh.Total)
    sz = [x*30 for x in sz]
    plt.grid(True)
    plt.scatter(gh.Total,y_coords, label='Total', s=sz)
    for i,country in enumerate(country_list):
        
        x_coord = total[i]
        y_coord = y_coords[i]
        if country == 'United States':
            country = 'USA'
        elif country == 'United Kingdom':
            country = 'UK'
        text = '%s (%d)'%(country, x_coord)
        fsize = 10 * (total[i]/100)
        if fsize < 10:
            fsize = 10
        #print('Fontsizes:', fsize)
        plt.text(x_coord,y_coord, text, fontsize=fsize)
    plt.title('Number of Hosted Websites per Country')
    plt.show()
    del plt
    
    
#aranks = []
colors = ['r','b','g','k','m']
files = ['AI','IO','ML']
files = ['AI']
hins = []

for file in files:
    data = pd.read_csv('D:/AI/Dataset/%s.csv'%file)
    #print('DATA:%s'%file)
    arankAnalysis(data)
    hin_df = hostedAnalysis(data)
    hins.append(hin_df)
    wset = kwordAnalysis(data,file)
'''
gh = pd.DataFrame(hins[0])
gh = gh.merge(hins[1],on='Country', how='outer')
gh = gh.merge(hins[2],on='Country', how='outer')

# Remove hostedIn row
gh = gh[ (gh.Country != 'hostedIn') ]

gh.fillna(value=0,inplace=True)
gh['Total'] = gh.Count_x + gh.Count_y + gh.Count
hostedplot(gh)
'''