# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 19:01:57 2018

@author: kkonakan
"""
import numpy as np
import kk_utils as kk

def rnp(s=1,S=10,sz=10):
    #return np.random.randint(s,S,size=(1,sz))
    import random
    return [random.randint(s,S) for i in range(sz+1)]

kk.plot3D(rnp(),rnp(),np.array(rnp()),scatter=False)