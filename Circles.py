# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 20:05:16 2018

@author: kkonakan
"""

import sklearn as sk
import sklearn.datasets as skd
import sklearn.metrics as skmt
import numpy as np
import kk_utils as kk
import matplotlib.pyplot as plt
import time

bscores=[]
linscores = []
logscores = []

linreg = sk.linear_model.LinearRegression()
logreg = sk.linear_model.LogisticRegressionCV()
breg = sk.naive_bayes.GaussianNB()
st = time.time()
X,Y = skd.make_moons(n_samples=10000,random_state=123)
X_train,X_test, Y_train,Y_test = skm.train_test_split(X, Y, \
                                        test_size=0.3,random_state=123)
    
sc, linreg = kk.fitModel(linreg,X,Y,roc_stats=False)
sc, logreg = kk.fitModel(logreg,X,Y,roc_stats=False)
sc, breg = kk.fitModel(breg,X,Y,roc_stats=False)

kk.compare_models([linreg, logreg,breg], X_test,Y_test)
'''
for i in range(1,20):
    samples = 1000 * i
    print('Number of samples:',samples)
    X,Y = skd.make_moons(n_samples=samples,random_state=123)
    
    #X,Y = skd.make_circles(n_samples=1000)
    
    #kk.plot2D(X,properties=False)
    linscores.append(kk.fitModel(linreg, X,Y))
    logscores.append(kk.fitModel(logreg, X,Y))
    bscores.append(kk.fitModel(breg, X,Y))
    
print('Calculating scores took %f seconds'%(time.time()-st))
kk.scorePlot(linscores, title='Linear Reg Scores plot')
kk.scorePlot(logscores, title='Log Reg Scores plot')
kk.scorePlot(bscores, title='Bayes Reg Scores plot')
Y = np.arange(len(linscores))
plt.figure(figsize=(8,8))
plt.plot(Y, linscores, label='Linear Reg', color='r')
plt.plot(Y, logscores, label='Logistic Reg', color='k')
plt.plot(Y, bscores, label='Bayes Reg', color='m')
plt.legend(loc='upper right')
plt.show()
del plt
print('Finished in %f seconds'%(time.time()-st))
'''