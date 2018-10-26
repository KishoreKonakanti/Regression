# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 19:06:30 2018

@author: kkonakan
"""

import urllib
import re
import bs4

def download(url):
    html = None
    soup = None
    try:
        html = urllib.request.urlopen(url).read()        
        soup = bs4.BeautifulSoup(html,'lxml')
    except Exception: pass
    return html,soup

def retrieveGRank(url):
    base_url = 'https://www.alexa.com/siteinfo/'
    comp_url = base_url+url
    html,_ = download(comp_url)
    html = str(html)
    rank = None
    try:
        rank = re.findall('.*global\":([\d].*?)}.*',html)[0]
        print('Rank:',rank)
        return rank
    except Exception:
        return None
    
print(retrieveGRank('vernacular.ai'))