# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 20:44:23 2018

@author: kkonakan
"""

import numpy as np
import pandas as pd
import sklearn.model_selection as skm
from sklearn.utils import check_random_state
import sklearn.datasets as skd

ENULL = -1
ESHAPE = -2
EINVAL = -3 # Invalid input

def getDatasets(binary=False):
    binaryData = [skd.load_breast_cancer(), skd.load_digits(), skd.load_iris()]    
    All = [skd.load_boston(),skd.load_diabetes()]
    All.extend(binaryData)
    print(type(All), len(All))
    if binary is True:
        return binaryData
    return All

def fitModel(model, X, Y, test_size=0.3,cv=True,ncv=10):
    X_train,X_test, Y_train,Y_test = skm.train_test_split(X, Y, \
                                        test_size=test_size,random_state=123)
    model.fit(X,Y)
    if cv is True:
        scores = skm.cross_val_score(model, X,Y,cv=ncv)
        return (round(np.max(scores)*100,2), np.argmax(scores))    
    return round(model.score(X_test,Y_test),2)

def MeanNormalizer1D(X):
    '''
        Mean Normalizer:
            for x in X:
                x_dash = x - avg(X)/(max(X) - min(X))
    '''
    if(checkNone(X) is True):
        return None
    mean = np.mean(X)
    denom = np.max(X) - np.min(X)
    if denom != 0:
        X = (X - mean) / denom
    return X

def MeanNormalizer(X):
    '''
        Generic Mean Normalizer
    '''
    if len(X.shape) == 1:
        return MeanNormalizer1D(X)
    elif len(X.shape) == 2:
        return MeanNormalizer2D(X)
    else:
        print('Mean Normalizer not supported for >2 dimensions')
        return EINVAL
    
def MeanNormalizer2D(X):
    for i in range(X.shape[1]):
        X[:,i] = MeanNormalizer1D(X[:,i])
    return X
    
def checkNone(X):
    '''
        Checks if the data passed in an NULL array using np.all
        Returns TRUE if data is NULL
    '''
    type(np.all(X)) == type(None)

def plot2D(X,Y=None,title='Default Plot 2D',X_label='X',properties=True):
    import matplotlib.pyplot as plt
    L= len(X)
    #print('Length:',L)
    if Y is None:
        Y = np.array(list(range(L)))
        
    
    #(X,Y) = (Y,X)
    
    mean = round(np.mean(X),2)
    std = round(np.std(X),2)
    var = round(np.var(X),2)
    #print('Length of X, Y, Mean:',X.shape, Y.shape, Mean.shape)
    Mean = np.repeat(mean, repeats=L)
    plt.figure(figsize=(8,8))
    plt.scatter( Y,X,label=X_label)
    if properties is True:
        plt.plot(Y, Mean, color='r',label='MEAN:'+str(mean),linewidth=4)
        plt.plot(Y, np.repeat(var, repeats=L),linewidth=4, color='k',label='Variance:'+str(var))
        plt.plot(Y, np.repeat(std, repeats=L),linewidth=4, color='c',label='Std Dev:'+str(std))
    plt.title(title)
    
    plt.legend(loc='upper right', shadow=True)
    plt.show()
    del plt

def modelPlot(model, X, Y, title='Default Plot 2D'):
    '''
        Plots 2-D data
    '''
    if model is None:
        return EINVAL
    import matplotlib.pyplot as plt
    ypred = model.predict(X)
    plt.figure(figsize=(8,8))
    plt.scatter(range(len(Y)), Y, color='k', label='True')
    plt.plot(range(len(Y)), ypred, color='r', label='Predicted')
    #plt.plot(Y, np.repeat(np.mean(Y),repeats=np.max(Y)), color='c', linewidth=4,\
     #        label='MEAN')
    plt.legend(loc='upper right', shadow=True)
    plt.title(title)
    plt.show()
    del plt
    del model
    

def handleNans(X, strategy='mean'):
    if(strategy not in ('mean','median', 'most_frequent')):
        print('%s is not supported'%(strategy))
        print('Supported strategies:mean,median, most_frequent')
        return EINVAL
    from sklearn.preprocessing import Imputer
    return Imputer.fit_transform(X, strategy=strategy)

def split(X,Y, tr=70, tst=10, dev=20,rs=123):
    '''
        Since train_test_split does not return dev set, this function uses train_test_split
        to split according the set train/test/dev percentages:
            1. Diving data into train and test
            2. Further divide train into train and dev
    '''
    
    # Check for X,Y nulls, shapes
    # Data = X,Y
    # Shuffle using np.random.shuffle
    # Retreive wrt tr/tst/dev
    # Partition wrt tr/tst/dev
    if(tr+tst+dev != 100):
        print('%d+%d+%d is not 100 (instead its %d)'%(tr,tst,dev,(tr+tst+dev) ))
        return EINVAL
    if(checkNone(X) or checkNone(Y)):
        print ('X and/or Y cannot be NULLS') 
        return ENULL 
    elif(X.shape[0] != Y.shape[0]):
        print('dim1s of X and Y (%d != %d) are not aligned'%(X.shape[0],Y.shape[0]))
        return ESHAPE
    else:
        # To get consitent splits across different calls
        np.random.seed(rs)
        X_train, X_test,Y_train,Y_test = \
        skm.train_test_split(X,Y, test_size=(tst/100),\
                         random_state=check_random_state(rs))
        if(dev == 0):
            return (X_train, X_test,Y_train,Y_test )
        else:
            X_train,X_dev,Y_train,Y_dev = skm.train_test_split(X_train,Y_train, \
                    test_size=(dev/100), random_state=check_random_state(rs))
            return (X_train, X_test,X_dev, Y_train, Y_dev, Y_test )
        '''
        temp = np.hstack([X,Y])
        np.random.shuffle(temp)
        shuffled_X = temp[X.shape]
        shuffled_Y = temp[...,Y.shape]
        fdim  = temp.shape[0]
        train = (fdim*(tr/100))
        test = (fdim*(tst/100))
        dev = fdim*(dev/100)
        X_train,X_test,
        '''
             
def testcases():
    data = skd.load_boston()
    split(data.data, data.target)
testcases()