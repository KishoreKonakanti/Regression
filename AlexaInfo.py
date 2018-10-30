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
        html = urllib.request.urlopen(urllib.request.Request(url)).read()        
        soup = bs4.BeautifulSoup(html,'lxml')
    except Exception: 
        print('Error')
    return html,soup

def postingAds(html):
    H = str(html)
    print(H)
    if(H.find('ca-pub') > -1):
        return True
    else:
        return False

def retrieveGRank(html):
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

#html = urllib.request.urlopen(urllib.request.Request('www.greatandhra.com')).read()        
html,soup = download('https://www.greatandhra.com')
print('Posting Ads? ',postingAds(html))