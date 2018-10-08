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

dataset = skd.load_digits()
linreg = skl.LinearRegression()
Y = dataset.target
scores = []
pca = skD.PCA()
cv = 5
cvs = []
for n_components in range(60,65):
    print('Number of components:',n_components)
    pca = pca.set_params(n_components=n_components)    
    X = dataset.data
    X = kk.MeanNormalizer2D(X)
    X = pca.fit_transform(X)
    score,best_cv = kk.fitModel(linreg, X, Y, cv=True, ncv = 10)
    cvs.append(best_cv)
    scores.append(score)
    
# BEST SCORE CLASSIFICATION
pca = skD.PCA(n_components=61)
X = dataset.data
Y = dataset.target
X = kk.MeanNormalizer2D(X)
X = pca.fit_transform(X)
fsc = sk.model_selection.cross_val_score(linreg, X, Y, cv=10)
finalSc = round(np.max(fsc)*100,2)
print('CV count:', np.argmax(fsc))
print('Score:', finalSc)
