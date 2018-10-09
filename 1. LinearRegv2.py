# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 20:16:18 2018

@author: kkonakan
"""

import sklearn as sk
import sklearn.linear_model as skl
import sklearn.preprocessing as skp
import sklearn.datasets as skd
import sklearn.decomposition as skD
import numpy as np
import kk_utils as kk

dataset = skd.load_breast_cancer()

linreg = skl.LinearRegression()
rreg = skl.RidgeCV()
lasreg = skl.LassoCV()
logreg = skl.LogisticRegressionCV()

scores = []
'''
# Experimental Part
for n_components in range(60,65):
    print('Number of components:',n_components)
    pca = pca.set_params(n_components=n_components)    
    X = dataset.data
    X = kk.MeanNormalizer(X)
    X = pca.fit_transform(X)
    score,best_cv = kk.fitModel(linreg, X, Y, cv=True, ncv = 10)
    cvs.append(best_cv)
    scores.append(score)
   '''   
# BEST SCORE CLASSIFICATION
pca = skD.PCA()
for dataset in kk.getDatasets():
    print('Dataset Name:', dataset.DESCR[0:10])
    X = dataset.data
    Y = dataset.target
    #pca.set_params(n_components=X.shape[1]-2)
    X = pca.fit_transform(X)
    X = kk.MeanNormalizer(X) # This step makes a diff for Ridge and Lasso
    Y = dataset.target
    fsc = kk.fitModel(linreg, X, Y)
    print('Scores:%.2f, %.2f, %.2f, %.2f'%(kk.fitModel(linreg, X, Y), \
                                     kk.fitModel(rreg, X,Y), kk.fitModel(lasreg, X,Y),
                                     0.00))
