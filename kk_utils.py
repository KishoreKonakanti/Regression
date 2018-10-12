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

def fitModel(model, X, Y, test_size=0.3,cv=True,ncv=10, dsetProps=False, \
             plotModel=False, roc_stats=True):
    X_train,X_test, Y_train,Y_test = skm.train_test_split(X, Y, \
                                        test_size=test_size,random_state=123)
    if dsetProps is True:
        print('Summary:\n************************************')
        print('Number of columns:', X_train.shape[1])
        print('Shapes (Train, Test)')
        print('%d samples split into %d / %d samples'\
          %(X.shape[0],X_train.shape[0],X_test.shape[0]))
    #if(len(np.unique(Y)) == 2):
    #    print('BINARY TARGETS')
    #else:
    #    print('Number of classes:',len(np.unique(Y)))
    #print('Model Name:', model.__class__.__name__)
    score = 0
    model.fit(X,Y)
    if cv is True:
        scores = skm.cross_val_score(model, X,Y,cv=ncv)
        score = round(np.max(scores)*100,2)    
    score = round(model.score(X_test,Y_test)*100,2)
    if plotModel is True:
        modelPlot(model,X,Y,title='Score:'+str(score))
    #print('Score acheived:', score)
    if roc_stats is True:
        roc(model, X_test, Y_test)
    return score,model

def compare_models(models, X_test, Y_test):
    import sklearn.metrics as skmt
    import matplotlib.pyplot as plt
    num_models = len(models)
    auc_scores = []
    roc_curves = []
    print('Number of models:',num_models)
    
    # Plotting
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
    plt.figure(figsize=(8,8))
    roc = None
    for (i, model) in enumerate(models):
        if model is None:
            continue
        Y_score = model.predict(X_test)
        roc = np.array(skmt.roc_curve(Y_test, Y_score))
        #roc= np.where(roc < 1.0)
        auc = skmt.roc_auc_score(Y_test, Y_score)
        color = colors[i%8]
        print(type(roc), auc, len(roc),Y_test.shape)
        Y = roc[:,0]
        mName = model.__class__.__name__[0:10]
        #print(mName,auc,color)
        plt.plot(Y, roc[:,1], label= '%s ( AUC:%.2f )'%(mName,auc), color=color)
    plt.legend(loc='upper left',shadow=True)
    plt.show()
    del plt
    
def roc(model, X_test, Y_test):
    '''
        RECEIVER OPERATING CURVE
    '''
    print(Y_test.shape)
    import sklearn.metrics as skmt
    Y_score = model.predict(X_test)
    auc_score = skmt.roc_auc_score(Y_test, Y_score)
    plot2D(skmt.roc_curve(Y_test,Y_score),title='ROC Curve: ', X_label='AUC: %.2f'%(auc_score), scatter=False)
    return 0

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

def dataPlot(data_X, Y=None,title='Default Plot 2D',X_label='X',properties=False):
    plot2D(data_X, Y=None,title='Default Plot 2D',X_label='X',properties=False)
    return 0

def scorePlot(scores,title='Scores Plot'):
    X = np.arange(len(scores),dtype=int)
    Y = np.array(scores)
    import matplotlib.pyplot as plt
    plt.figure(figsize=(8,8))
    
    plt.plot(X,Y)
    plt.title(title)
    plt.show()
    del plt
    return 0
    
def plot2D(data_X, Y=None,title='Default Plot 2D',X_label='X',scatter=True, \
           properties=False):
    print(data_X.shape)
    if ( type(data_X ) != type(np.array(None))):
        data_X = np.array(data_X)
        
    if (len(data_X.shape) == 2):
            X = data_X[:,0]
            Y = data_X[:,1]   
    else:
        X = data_X
        
    import matplotlib.pyplot as plt
    L= len(X)
    print('Length:',L)
    if Y is None:
        Y = np.arange(L)
    print(X.shape, Y.shape)    
    mean = round(np.mean(X),2)
    std = round(np.std(X),2)
    var = round(np.var(X),2)
    Mean = np.repeat(mean, repeats=L)
    #print('Length of X, Y, Mean:',X.shape, Y.shape, Mean.shape)
    plt.figure(figsize=(8,8))
    if scatter is True:
        plt.scatter(Y, X, label=X_label)
    elif scatter is False:
        plt.plot(Y, X, label=X_label)
    #plt.plot(Y, X, label=X_label)
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