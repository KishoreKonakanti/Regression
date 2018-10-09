# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 23:17:18 2018

@author: kkonakan
"""
EINVAL = -1
def calBurnt(hrate, time, weight):
    '''
        Calories Burned = [(Age x 0.2017) + (Weight x 0.09036) + \
        (Heart Rate x 0.6309) - 55.0969] x Time / 4.184.
    '''
    if time >= 60:
        print ('Specify time in minutes')
        return EINVAL
    x = ((32*0.2017) + (weight*0.09036) + (hrate * 0.6309) - 55.0969) * (time/4.184)
    #x = x/4.184
    print('Total calories burnt:%f %f calories/min'%(x, x/time))

calBurnt(150,32,80)