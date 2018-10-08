# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 13:22:36 2018

@author: kkonakan
"""

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
    # Scaling and Centering
    if center is True:
        data = sk.preprocessing.StandardScaler().fit_transform(data)
    if scale is True:
        var_data = np.std(data.data)
        var_data *= var_data
        var_thres = var_data*0.1
        sks = sk.feature_selection.VarianceThreshold(threshold=var_thres)
        data = sks.fit_transform(data)
    return data
    
def fitdata(boston, dname,prep=True, plots=False):
    global datascores
    datascores = {}
    X = boston.data
    Y = boston.target
    
    if prep is True:
        X = prepocessing(X)
    
    X_train, X_test, Y_train, Y_test= sk.model_selection.train_test_split(X,Y,\
                                                        test_size=0.25)    
    lCV = Lasso()    
    lCV.fit(X_train,Y_train)
    #cross_val_score(lr, X, Y, scoring='accuracy', cv=10)
    if plots is False:        
        return '%.2f'%(lCV.score(X_test,Y_test)*100)
    else:
        title = dname + '=>' +model.__class__.__name__.upper()
       # kk.modelPlot(lCV, X_test, Y_test, title + '-Test')
            
    print('lCV Regression Expression:')
    printExp(lCV)
    return '%.2f'%(lCV.score(X_test,Y_test)*100)
    '''
    
    '''

print('No Preprocessing', \
      fitdata(skd.load_boston(),'BOSTON DATASET', prep=False,plots=False))
print('With Preprocessing',\
      fitdata(skd.load_boston(),'BOSTON DATASET', prep=True,plots=True))

'''
for (k,v) in datascores.items():
    v = [round(x,2) for x in v]
    print(k,'=>',v)
    '''