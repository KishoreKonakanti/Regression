# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 16:30:32 2018

@author: kkonakan
"""

import sklearn as sk
import sklearn.datasets as skd
import sklearn.cluster as skc
import numpy as np

def plot(X,Y): 
    centers = np.unique(Y)
    clusters=[]

    i = 0

    if centers is not None:
        for centre in centers:        
            temp = np.array( np.where( Y == centre ) )
            temp = np.ravel(temp)
            clusters.append(X[temp])
    #print (clusters)
    import matplotlib.pyplot as plt
    plt.figure(figsize=(8,8))
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
    markers = ['o', '^', 'v','<','>','1','2','3','4','s','p','P', '*','h',
               'H','+','x','X','D','d','|','_',0,1,2,3,4,5,6,7,8,9,10,11]
    
    for (i,cluster) in enumerate(clusters):
        color = colors[ i%8 ]
        marker = markers [ i % 35 ]
        #print('Cluster shape:',cluster.shape)
        plt.scatter(cluster[:,0], cluster[:,1], c=color, marker=marker)
    plt.grid(True)
    plt.show()
    del plt
    
X,Y = skd.make_blobs(centers=4,random_state=123)
kmeans = skc.KMeans(n_clusters=4)
ypred = kmeans.fit_predict(X)
#print(Y,X.shape,Y.shape)

plot(X,Y)
plot(X,ypred)