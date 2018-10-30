# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 16:40:03 2018

@author: kkonakan
"""

import sklearn as sk
import sklearn.preprocessing as skp
import sklearn.linear_model as skl
import numpy as np
import sklearn.datasets as skd
import kk_utils as kk
import sklearn.tree as skt


def trailAndError(M):
    scores = {}
    n_texamples = 100
    print('Training set/Dimension Count/Tree Depth:')
    for i in range(1,M+1):
        model = skt.DecisionTreeRegressor(max_depth=i)
        m = 100 * i
        n_f = 10*i
        n_classes = i
        if(n_f > 10**6):
            n_f = 10**6
        print('%d - %d - %d'%(n_texamples,n_f,m))
        (X,Y) = kk.genData(n_features=n_f, n_classes=n_classes,m=n_texamples,target='C')
        sc,_ = kk.fitModel(model, X, Y,cv=False,ncv=0, roc_stats=False)
        scores[i] = sc
        if sc < 100:
            print('***************Score is ',sc)
        del model
    import matplotlib.pyplot as plt
    plt.plot(scores.keys(), scores.values())
    plt.xlabel('Max Depth')
    plt.ylabel('Score')
    plt.grid(True)
    plt.show()
    del plt
    kk.plot2D(scores.keys(), scores.values(),\
              X_label='Score', Y_label='Max Depth', scatter=False)

import time
st = time.time()
trailAndError(30)
print('Time taken:', (time.time() - st), 'seconds')
'''
for dataset in kk.getDatasets():
    model = skt.DecisionTreeClassifier()
    print('Dataset Name:', dataset.DESCR[0:10])
    X = dataset.data
    Y = dataset.target
    kk.fitModel(model, X,Y, dsetProps=True, roc_stats=False)
    '''