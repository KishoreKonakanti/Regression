# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 11:26:52 2018

@author: kkonakan
"""

import urllib.request as ureq
import re

def download(url):
    content = ureq.urlopen(url).read()
    return content

def saveHTML(url, content):
    print(url, content)
    fname = path
    try:
        site = re.findall('http[s]{0,1}://www.([\w\W\d]{1,}).ai', url)[0]
        fname = path+site+'.html'
        print(fname)
        ufile = open(fname, 'w')
        ufile.write(str(content))
        ufile.close()
    except Exception:
        print('Error occured druing %s saving'%url)

path = 'D:/AI/DataSet/'
url = 'http://www.google.com'
content = download(url)
saveHTML(url, content)