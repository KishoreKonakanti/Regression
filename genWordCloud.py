# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 18:03:54 2018

@author: kkonakan
"""

import pandas as pd
from wordcloud import WordCloud
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from langdetect import detect_langs
from langdetect import DetectorFactory
import langid as lid

DetectorFactory.seed = 0
nonEng = []
EngWords = []
def langList(words):
    dls= []
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
            print('*****************',word)
            print(e)
    return dls    

def genWordCloud(wordSet):
    kwstr = ''
    for word in wordSet:
        kwstr = kwstr + ' '+ word
        
    print('Number of key words:',len(wordSet))
    print('Number of key words:',len(kwstr))
    
    wordcloud = WordCloud(width = 800, height = 800,\
                          background_color ='white',  \
                          stopwords = sw,  \
                          min_font_size = 10).generate(kwstr)
    plt.figure(figsize=(10,10))
    plt.imshow(wordcloud)
    plt.show()    

df = pd.read_csv('D:/AI/Dataset/IO.csv')
kwords = df['kwords']
kwords = kwords.dropna()

wordSet = set()
sw = stopwords.words('english')
print('Reading lines')
for line in kwords:
    tokens = word_tokenize(line)
    [wordSet.add(word) for word in tokens]


wordSet = wordSet.difference(sw)
genWordCloud(wordSet)