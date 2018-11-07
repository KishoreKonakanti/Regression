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
from langdetect import DetectorFactory
import langid as lid

DetectorFactory.seed = 0
nonEng = []
EngWords = []


# noinspection SpellCheckingInspection
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


# noinspection SpellCheckingInspection
def genwordcloud(wordset):
    if wordset is None:
        return None
    kwstr = ''
    for word in wordset:
        kwstr = kwstr + ' ' + word

    print('Number of key words:', len(wordset))
    print('Length of the string:', len(kwstr))

    wordcloud = WordCloud(width=800, height=800, background_color='white',\
                          stopwords=sw, min_font_size=10).generate(kwstr)
    plt.figure(figsize=(10, 10))
    plt.imshow(wordcloud)
    plt.show()


df = pd.read_csv('D:/AI/Dataset/AI.csv')
print(df)
kwords = df['kwords']
kwords = kwords.dropna()

wordset = set()
sw = stopwords.words('english')
print('Reading lines')
for line in kwords:
    tokens = word_tokenize(line)
    [wordset.add(word) for word in tokens]

wordset = wordSet.difference(sw)
genWordCloud(wordset)
