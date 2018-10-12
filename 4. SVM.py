# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 21:07:29 2018

@author: kkonakan
"""

import sklearn as sk
import sklearn.datasets as skd
import sklearn.svm as svm
import kk_utils as kk
from sklearn.metrics import roc_curve,roc_auc_score

(X,Y) = skd.make_classification(n_features=4,n_samples=100)
X_train,X_test, Y_train,Y_test = sk.model_selection.train_test_split(X, Y, \
                                        test_size=0.3,random_state=123)
svcl = svm.SVC(kernel='linear')
svcr = svm.SVC(kernel='rbf')
logreg = sk.linear_model.LogisticRegressionCV()
model = logreg
kk.fitModel(svcl, X,Y, plotModel=True, roc_stats=True)
#kk.fitModel(svcr, X,Y, plotModel=True)
