# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 16:23:32 2018

@author: kkonakan
"""

def urlparser(url):
    import re
    try:
        pattern = 'http[s]{0,1}://[w.]{0,4}([\w\W\d]{1,})\.*\.ai'
    
        website= re.findall(pattern, url)[0]
    except Exception:
        website = None
    return website
def getRecorded():
    file= open('D:/AI/Links.txt','r')
    tset = set()
    for address in file.readlines():
        website = urlparser(address)
        if website is not None:
            tset.add(website)
    file.close()
    return tset

def getUniq(fname):
    file = open(fname,'r')
    siteSet = set()
    for site in file.readlines():
        website = urlparser(site)
        if  website is not None:
            siteSet.add(website)
        else:
            print('!!!!!!!%s is a duplicate!!!!!'%site)
            
    file.close()
    return siteSet
    
ll1 = getUniq('D:/AI/linklist.txt')
ll2 = getUniq('D:/AI/temp.txt')
ll3 = getUniq('D:/AI/temp1.txt')