# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 15:33:22 2018

@author: kkonakan
"""

import numpy as np
import sklearn.datasets as skd
import kk_utils as kk

def genData(x,y,binary=True, numClasses=2):
    data = np.random.random(size=(x,y))
    if binary is True:
        target = np.random.randint(0,numClasses+1,size=(1,y))
    else:
        target = np.random.random(size=(1,y))
    return (data,target)

X = skd.load_boston()
print(X.shape)