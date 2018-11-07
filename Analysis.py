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
import langid as lid

DetectorFactory.seed = 0
nonEng = []
EngWords = []

def langlist(words):
    dls = []
    for word in words:
        try:
            lang = lid.classify(word)[0]
            if lang != 'en':
                nonEng.append(word)
                continue
            else:
                EngWords.append(word)
            dls.append(lid.classify(word))
        except Exception as e:
            print('*****************', word)
            print(e)
    return dls


def genwordcloud(wordset):
    print('Incoming:',wordset)
    if wordset is None:
        return None
    kwstr = ''
    for word in wordset:
        kwstr = kwstr + ' ' + word

    print('Number of key words:', len(wordset))
    print('Length of the string:', len(kwstr))

    wordcloud = WordCloud(width=800, height=800, background_color='white', 
                          stopwords=stopwords.words('english'), min_font_size=10).generate(kwstr)
    plt.figure(figsize=(10, 10))
    plt.imshow(wordcloud)
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
    #plt.scatter(scaledar,list(range(len(scaledar))), c=colors.pop(),label='AI')
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
    print(hin_dict.shape)
   # hin_dict.plot()
    
    return hin_dict

def kwordAnalysis(df):
    kwords = df.kwords
    kwords.dropna(inplace=True)
    wordset = set()
    sw = stopwords.words('english')
    import re
    pattern='[\w\W\d]{0,}[a-zA-Z]{1,}[\w\W\d].*'
    for line in kwords:
        for word in line:
            if re.match(pattern, word): 
                wordset.add(word)
    
    wordset.difference_update(sw)
    genwordcloud(wordset)
    del wordset
    
def hostedplot(gh):
    country_list = list(gh.Country)
    total = list(gh.Total)
    y_coords = np.arange(len(gh))
    import matplotlib.pyplot as plt

    plt.figure(figsize=(14,14))
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
        fsize = 10 * (total[i]/100)
        if fsize < 10:
            fsize = 10
        #print('Fontsizes:', fsize)
        plt.text(x_coord,y_coord,country, fontsize=fsize)
        
    plt.show()
    del plt
    
    
#aranks = []
colors = ['r','b','g','k','m']
files = ['AI','IO','ML']
hins = []

for file in files:
    data = pd.read_csv('D:/AI/Dataset/%s.csv'%file)
    print('DATA:%s'%file)
    #arankAnalysis(data)
    hin_df = hostedAnalysis(data)
    hins.append(hin_df)
    
   # print('Number of countries',len(hin_df))
    kwordAnalysis(data)
#    print('Mean :%f and Standard Deviation:%f,Variance:%f'%(arankAnalysis(data)))

gh = pd.DataFrame(hins[0])
gh = gh.merge(hins[1],on='Country', how='outer')
gh = gh.merge(hins[2],on='Country', how='outer')
gh.fillna(value=0,inplace=True)
gh['Total'] = gh.Count_x + gh.Count_y + gh.Count
hostedplot(gh)
# Hosted Analysis plot
#import matplotlib.pyplot as plt
