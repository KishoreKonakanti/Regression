# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 20:36:32 2018

@author: kkonakan
"""

import re

ai = open('D:/AI/AI.txt','a')
ml = open('D:/AI/ML.txt','a')
io = open('D:/AI/IO.txt','a')

def transform(fname):
    file = open('D:/AI/%s.txt'%fname)
    pattern = 'http[s]{0,1}://[w.]{0,4}.[\w\W\d]*?\.ai'
    ext_pattern = 'http[s]{0,1}://[w.]{0,4}.([\w\W\d]*?)\.ai/.*'
    for line in file.readlines():
        if(re.match(pattern, line)):
            print(line)
        elif(re.match(ext_pattern, line)):
            base = re.findall(ext_pattern,line)[0]
            print('https://www.%s.ai'%base)
        else:pass
        

