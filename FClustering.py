# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 19:28:42 2018

@author: kkonakan
"""

import sklearn.datasets as skd
import sklearn.cluster as skc
import sklearn.metrics as skm
import sklearn.neighbors as skn
from sklearn.mixture import GaussianMixture as gm
import numpy as np
import kk_utils as kk

import time
'''
intertias = []
for n_clusters in range(101,151 ):
    print('Number of clusters: %d'%n_clusters)
    km = skc.KMeans(n_clusters=n_clusters)
    km.fit(X)
    intertias.append(km.inertia_)
    del km

kk.plot2D(intertias, scatter=False, X_label='Number of clusters', Y_label='Intertias')
'''

def getHScore(models):    
    global X,Y
    for model in models:        
        if model is None:
            continue
        mName = model.__class__.__name__
        try:
            model.fit(X,Y)
            Ypred = model.predict(X)
        except AttributeError:
            Ypred = model.fit_predict(X)
        except AttributeError:
            model.fit(X)
            Ypred = model.labels_
        except Exception:
            print('Couldnt find either fit or fit_predict model for %s...'%mName)
        finally:
            print(':)')
        print('Model Name:', mName)
 #       kk.clusterPlot(X,Ypred, title=mName)
     #   print('Adj Rand Score:%.2f'%skm.adjusted_rand_score(Y,Ypred))
        print('Homogenity score:%.2f'%skm.homogeneity_score(Y,Ypred))
        print('*****************************************************')
        del model
    

st = time.time()
n_clusters=20
for factor in np.arange(0,1,0.1):
    print('FACTOR:', factor)
    #(X,Y) = skd.make_blobs(n_samples = 30000, centers= 30)
    (X,Y) = skd.make_circles(n_samples=300, noise=0.02, random_state=123,factor=factor)
    #(X,Y) = skd.make_moons(n_samples=1000, noise=0.05)
    skd.make_circles()
    #kk.clusterPlot(X,Y, title='Clusters in different colors')
    km = skc.KMeans(n_clusters=n_clusters)
    db = skc.DBSCAN(eps=0.1)
    sac = skc.AgglomerativeClustering(n_clusters=n_clusters, linkage='single')
    aac = skc.AgglomerativeClustering(n_clusters=n_clusters, linkage='average')
    wac = skc.AgglomerativeClustering(n_clusters=n_clusters, linkage='ward')
    cac = skc.AgglomerativeClustering( n_clusters=n_clusters,linkage='complete')
    #sc = skc.SpectralClustering()
    #sbc = skc.SpectralCoclustering()
    getHScore([km, sac,aac, wac, cac, db])
    print('Total time taken: %d seconds'%(time.time() - st))