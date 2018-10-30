# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 12:04:10 2018

@author: kkonakan
"""

import sklearn as sk
import sklearn.preprocessing as skp
import sklearn.model_selection as skm
import sklearn.linear_model as skl
import sklearn.feature_selection as skf
import sklearn.datasets as skd
import pandas as pd
import numpy as np
import kk_utils as kk



def LogReg():
    logregCV = skl.LogisticRegressionCV()
    
    for dataset in kk.getDatasets(binary=True):
        print('Dataset Name:',dataset.DESCR[0:10])
        X = dataset.data
        Y = dataset.target
        X_scaled = skp.scale(X)
        logreg = logregCV
        print('Without Preprocessing Score:',kk.fitModel(logreg, X, Y))
        print('With Preprocessing Score:',kk.fitModel(logreg, X_scaled,Y))


def LinearReg():
    linreg = skl.LinearRegression()
    
    for dataset in kk.getDatasets(binary=False):
        print('Dataset Name:',dataset.DESCR[0:10])
        X = dataset.data
        Y = dataset.target
        X_scaled = skp.scale(X)
        print('Without Preprocessing Score:',kk.fitModel(linreg, X, Y))
        print('With Preprocessing Score:',kk.fitModel(linreg, X_scaled,Y))

LinearReg()
'''
X_train = scaler.fit_transform(X_train)
Y_train = scaler.fit_transform(Y_train)

logreg.fit(X_train,Y_train)
'''
#print('Post preprocessing score:',logreg.score(X_test, Y_test))

'''
# Centering
skv = skf.VarianceThreshold(threshold=1.5)
dataset = skv.fit_transform(dataset)
Y_center = dataset.target
print(Y_center.shape)

#kk.plot2D(list(range(len(Y_scaled))),Y_scaled, 'Variance Thresholded')
# Scaling
#sks = skp.StandardScaler()
#Y_scaled = sks.fit_transform(Y)
'''
