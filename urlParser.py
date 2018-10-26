# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 15:22:45 2018

@author: kkonakan
"""

def urlparser(url):
    print('Incoming ',url)
    import re
    pattern = 'http[s]{0,1}://[w]{0,3}.([\w\W\d]{1,})\.*\.ai'
    
    website= re.findall(pattern, url)[0]
    print('URL:%s->%s'%(url,website))
    return website
    
def testcases():
    urls = ['http://www.nos.ai',
            'https://www.withs.ai',
            'http://www.3ws.ai',
            'http://ww.2ws.ai',
            'http://w.1w.ai',
            'https://www.2dots.2sot.ai',
            'https://www.3dots.3dots.ai',
            'https://www.hyp-hen.ai',
            'https://www.knownone.ai/link']
    for url in urls:
        urlparser(url)
    
testcases()