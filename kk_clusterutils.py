# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 16:30:32 2018

@author: kkonakan
"""

import sklearn.datasets as skd
import sklearn.cluster as skc
import sklearn.metrics as skm
import numpy as np
import kk_utils as kk

    
def fitModel(model): 
    if model is None:
        assert('Model cannot be Null')
#    mName=model.__class__.__name__
    hscores = []
    for n_clusters in range(1,5):
        n_samples = n_clusters * 1000
        #X,Y = kk.genData(m=n_samples, n_classes=n_clusters, n_features=10)
        X, Y = skd.make_blobs(n_samples=n_samples, centers=n_clusters,random_state=123)
        Ypred = model.fit_predict(X)
        kk.clusterValidatePlot(X,Y,Ypred,title='Original with %d clusters '%(n_clusters))
        print('Number of clusters: %d'%n_clusters)
        hscores.append(skm.homogeneity_score(Y,Ypred))
        #print(Y, Ypred)
        del Y, Ypred,X
    #print(hscores)    
    #kk.scorePlot(hscores, title='HScores with '+mName,X_t = 'Number of clusters', Y_t='HScore')
    return hscores

import time
st = time.time()
kms = fitModel(skc.KMeans())
ac = skc.AgglomerativeClustering(linkage='single')
Y = list(range(len(dbs)))
import matplotlib.pyplot as plt
plt.figure(figsize=(8,8))
plt.plot(Y,kms,label='K Means')
plt.plot(Y,dbs,label='DBSCAN')
plt.grid(True)
plt.title('Comparison of Homogenity scores')
plt.legend(loc='upper right',fontsize='x-large')
plt.show()
print('Total  time taken:%d seconds'%(time.time() - st))