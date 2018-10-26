# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 15:19:53 2018

@author: kkonakan
"""

import nltk.corpus as nc
from nltk.corpus import brown

fname = 'milton-paradise.txt'
guten = nc.gutenberg
print(guten.fileids())
print(len(guten.raw(fname)))
print(guten.sents(fname)[0:5])
print(guten.words(fname)[0:10])
print(brown.categories())