# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 21:07:29 2018

@author: kkonakan
"""

import sklearn as sk
import sklearn.datasets as skd
import sklearn.svm as svm
import kk_utils as kk
import numpy as np
from sklearn.metrics import roc_curve,roc_auc_score

Lscores = []
Rscores = []
Pscores = []
Sscores = []
for i in range(1,50):
    num_dims = 10*i
    n_samples=2**i
    (X,Y) = skd.make_moons(n_samples=n_samples)
    X_train, X_test, Y_train, Y_test = sk.model_selection.train_test_split(X, Y, \
                                            test_size=0.3,random_state=123)
    
    svcl = svm.SVC(kernel='linear')
    svcr = svm.SVC(kernel='rbf')
    svcp = svm.SVC(kernel='poly')
    svcsig = svm.SVC(kernel='sigmoid')
    
    scl,_ = kk.fitModel(svcl, X,Y, plotModel=False, roc_stats=False)
    scr,_ = kk.fitModel(svcr, X,Y, plotModel=False, roc_stats=False)
    scp,_ = kk.fitModel(svcp, X,Y, plotModel=False, roc_stats=False)
    scs,_ = kk.fitModel(svcsig, X,Y, plotModel=False, roc_stats=False)
    
    #kk.compare_models([svcl,svcr,svcp,svcsig], X_test, Y_test)
    
    #print(svcl.support_vectors_)
    Pscores.append(scp)
    Sscores.append(scs)
    Lscores.append(scl)
    Rscores.append(scr)
    #print('Scores:%f %f'%(scl,scr))

Y = list(range(1, len(Lscores)+1))
Y = np.multiply(Y, 10)
import matplotlib.pyplot as plt
plt.figure(figsize=(10,10))
#plt.scatter(Rscores, Lscores)

plt.plot(Y, Lscores,'g', label='Linear')
plt.plot(Y, Rscores,'r',label='RBF')
plt.plot(Y, Pscores,'b',label='Polynomial')
plt.plot(Y, Sscores,'k', label='Sigmoid')

plt.xlabel('Number of samples')
plt.ylabel('Accuracy')
plt.title('SVM Kernel Comparison')
plt.legend(loc='upper right', fontsize='x-large')
plt.grid(True)
del plt