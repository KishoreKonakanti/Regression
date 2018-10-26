# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 01:19:50 2018

@author: kkonakan
"""

import re


def urlparser(url):
    try:
        pattern = 'http[s]{0,1}://[w.]{0,4}([\w\W\d]{1,})\.*\.ai'
        website= re.findall(pattern, url)[0]
        if website.find('yahoo') > 0: # Yahoo search query should nt be recorded
            website = None
    except IndexError:
        website = None
    return website

def mge():
    Lset = set()
    fnames = ['Baidu', 'Bing', 'Yahoo']
    for fname in fnames:
        fname = 'D:/AI/%s.txt'%fname
        final = 'D:/AI/%s.txt'%final
        file = open(fname,'r')
        final = open(final,'a')
        for link in file.readlines():
            siteName = urlparser(link)
            if siteName is not None and siteName not in Lset:
                
                Lset.add(siteName)
        file.close()
    return Lset
final = 'Final.txt'
print(len(mge()))