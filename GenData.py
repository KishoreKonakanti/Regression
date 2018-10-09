# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 15:33:22 2018

@author: kkonakan
"""

import numpy as np

def genData(x,y,binary=True, numClasses=2):
    data = np.random.random(size=(x,y))
    if binary is True:
        target = np.random.randint(0,numClasses+1,size=(x,y))
    else:
        target = np.random.random(size=(x,y))
    return (data,target)

print(genData(5,5,numClasses=5))
print(genData(2,2, False))