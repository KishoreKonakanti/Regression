# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 22:21:18 2018

@author: kkonakan
"""

import kk_utils as kk
import sklearn as sk
import sklearn.datasets as skd
import numpy as np
import sklearn.cluster as skc

for num_centers in range(1,11):
    X, Y = skd.make_blobs(n_samples=10000, n_features=10, centers=4)
    kk.plot2D(X,title='Centers'+str(num_centers))
    print('DONE')

kmeans = skc.KMeans()
kmeans.fit(X)
