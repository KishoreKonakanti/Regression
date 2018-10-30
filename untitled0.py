# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 01:05:44 2018

@author: kkonakan
"""

def urlparser(url):
    try:
        pattern = 'http[s]{0,1}://[w.]{0,4}([\w\W\d]{1,})\.*\.ai'
        website= re.findall(pattern, url)[0]
        if website.find('yahoo') > 0: # Yahoo search query should nt be recorded
            website = None
    except IndexError:
        website = None
    return website
	
def merge():
	global Lset
	for fl in ['Baidu.txt','Yahoo.txt','Bing.txt']:
        fname = 'D:/AI/%s'%fl
		file = open(fname, 'r')
		for link in file.readlines():
			name = urlparser(link)
			if name is not None and name not in Lset:
				Lset.add(name)
		file.close()

Lset = set()
print(len(Lset))