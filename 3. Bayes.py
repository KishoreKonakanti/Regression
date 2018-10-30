# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 23:17:17 2018

@author: kkonakan
"""

#import sklearn as sk
import kk_utils as kk
import sklearn.linear_model as skl
#import sklearn.datasets as skd
import sklearn.decomposition as skD
#import sklearn.model_selection as skm
#import sklearn.preprocessing as skp
import sklearn.naive_bayes as skn
import numpy as np

bayes = skl.BayesianRidge(compute_score=True)
pca = skD.PCA()
cnt = 1
'''
for dataset in kk.getDatasets():
    cnt = cnt+1
    print ('Dataset Name:',dataset.DESCR[0:10])
    X = dataset.data
    Y = dataset.target
    X = kk.MeanNormalizer(X)
    n_comp = X.shape[1] - cnt
    if n_comp <= 0:
        n_comp = X.shape[1]
    pca.set_params(n_components = n_comp)
    X = pca.fit_transform(X)
    print('Score:',kk.fitModel(bayes, X, Y))
    del X,Y
'''
gauss = skn.GaussianNB()
bernoulli =skn.BernoulliNB()
multi = skn.MultinomialNB()
for dataset in kk.getDatasets(binary=True):
    #dataset = skd.load_breast_cancer()
    print ('Dataset Name:',dataset.DESCR[0:20],'\n=================================')
    X = dataset.data + np.random.random(size=(dataset.data.shape))
    Y = dataset.target
    if(len(np.unique(Y)) > 2):
        bernoulli.set_params(binarize=True)
    else:
        print('Binary Classification')
    X = kk.MeanNormalizer(X)
    pca.set_params(n_components=np.random.randint(1, X.shape[1]+1))
    X = pca.fit_transform(X)
    kk.fitModel(bayes,X,Y)
    kk.fitModel(gauss, X, Y,dsetProps=False)
    kk.fitModel(bernoulli, X, Y, dsetProps=False)
    #kk.fitModel(multi, X, Y, dsetProps= False,cv=False)