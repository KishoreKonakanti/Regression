# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 20:05:49 2018

@author: kkonakan
"""

import csv
import numpy as np

def write(d):
    keys = ['a','b','c']
    with open('D:/demo.csv','a') as csvfile:
        writer = csv.DictWriter(csvfile, keys)
        writer.writeheader()
        writer.writerow(d)
       
d = {'a':10,'b':20,'c':30}
write(d)
write({'a':20,'c':np.NaN})