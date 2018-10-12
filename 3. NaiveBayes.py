# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 22:47:26 2018

@author: kkonakan
"""

import pandas as pd
import numpy as np

def calcProbs(data):
    #print('Incoming data:', data, data.shape[1])
    classes = np.unique(data)
    ncl = data.shape[1]
    probs = {}
    for cl in classes:
        f = len(data[np.where(data == cl)])
        probs[cl] = f/ncl
    return probs

def posterior():
    postprobs = np.array()
    for cl in classes:
        postprobs = prior * likelihood
    return np.argmax(postprobs)

def estimateLikelihood(X,Y):
    '''
        Gaussian: exp( -(x-mu_y)**2/ (2 * sigma_y*sigma_y )/sqrt(2*sigma_y*sigma_y * pi)
    '''
    mu_y = np.mean(Y)
    var_y = np.std(Y) * np.std(Y)
    
    t = (X - mu_y)**2
    t = np.exp(-t/(2*var_y))
    return t / np.sqrt(2*var_y*np.pi)
    
    
print(calcProbs(np.random.random((1,100))))