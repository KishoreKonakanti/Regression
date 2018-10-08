# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 20:32:36 2018

@author: kkonakan
"""

import sklearn.datasets as skd
from sklearn.linear_model import *
from sklearn.model_selection import cross_val_score
import kk_utils as kk
import pandas as pd
import sklearn as sk

datascores={}
def printExp(model):
    print('y = %.2f '%(model.intercept_))
    for (i,c) in enumerate(model.coef_):
        print('%.2f * x%d'%(c,i),)
     
def prepocessing(data, center=True, scale=True):
    # Mean
    if center is True:
        data = sk.preprocessing.StandardScaler().fit_transform(data)
    if scale is True:
        sks = sk.feature_selection.VarianceThreshold()
        data = sks.fit_transform(data)
    return data
    
def fitdata(boston, dname,prep=True, plots=False):
    global datascores
    datascores = {}
    X = boston.data
    Y = boston.target
    
    if prep is True:
        X = prepocessing(X)
    
    #X_train, X_test, X_test, Y_train, Y_test, Y_test = kk.split(X,Y)
    X_train, X_test, Y_train, Y_test= sk.model_selection.train_test_split(X,Y,\
                                                        test_size=0.25)
    
    #print('Shapes:', X_train.shape, X_test.shape, X_test.shape)
    
    # Models
    lr = LinearRegression()
    rCV = RidgeCV()
    lCV = Lasso()
    
    lr.fit(X_train,Y_train)
    rCV.fit(X_train,Y_train)
    lCV.fit(X_train,Y_train)
    #cross_val_score(lr, X, Y, scoring='accuracy', cv=10)
    scores = [lr.score(X_test,Y_test)*100, rCV.score(X_test,Y_test)*100,
              lCV.score(X_test,Y_test)*100]
    datascores[dname] = scores
    threshold=79.
    if plots is False:
        return datascores
    else:
        # Continue
        pass
    if(scores[0] > threshold or scores[1] > threshold or scores[2] > threshold):
        # Plot graphs and print Expressions
        title = ''
        for model in (lr, rCV, lCV):
            title = dname + '=>' +model.__class__.__name__.upper()
            kk.modelPlot(model, X_test, Y_test, title + '-Test')
            #kk.modelPlot(model, X_test, Y_test, title + '-DEV')
            #kk.modelPlot(model, X_train, Y_train, title + '-Train')
        '''
        print('Linear Regression Expression:')
        printExp(lr)
        print('Ridge Regression Expression:')
        printExp(rCV)
        print('lCV Regression Expression:')
        printExp(lCV)
        '''
    else:
        title = ''
        for model in (lr, rCV, lCV):
            title = dname + ': '+model.__class__.__name__
            kk.modelPlot(model, X_test, Y_test, title + '- TEST')
        print('Linear Reg: %f\nRidge: %f\nlCV: %f'%(lr.score(X_test,Y_test)*100, 
                                                  rCV.score(X_test,Y_test)*100,
                                                  lCV.score(X_test,Y_test)*100))
    return datascores
    '''
    
    '''

#boston = skd.load_breast_cancer()
#fitdata(skd.load_breast_cancer(), 'BREAST CANCER')
print('No Preprocessing', \
      fitdata(skd.load_iris(),'IRIS DATASET', prep=False,plots=False))
print('With Preprocessing',\
      fitdata(skd.load_iris(),'IRIS DATASET', prep=True,plots=True))
#fitdata(skd.load_boston(),'BOSTON DATASET', prep=True)
#fitdata(skd.load_diabetes(),'DIABETES')
#fitdata(skd.load_digits(),'DIGITS')
#fitdata(skd.load_iris(), 'IRIS')
'''
for (k,v) in datascores.items():
    v = [round(x,2) for x in v]
    print(k,'=>',v)
    '''