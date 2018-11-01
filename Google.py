# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 12:23:05 2018

@author: kkonakan
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 12:16:10 2018

@author: kkonakan
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 20:41:55 2018

@author: kkonakan
"""

import urllib.request as ureq
import urllib
import bs4
import re


path = 'D:/AI/DataSet/'

def download(url):
    soup = None
    html = None
    try:
        html = ureq.urlopen(ureq.Request(url,headers={'User-agent':'Mozilla/5.0'})).read()
        soup = bs4.BeautifulSoup(html,'lxml')
    except urllib.request.HTTPError:
        print('Error:',ureq.HTTPError)
        print(url,' site is not allowing bots')
    return html,soup

def linkExtraction(soup):
    global rc
    link_set = set()
    for user in soup.find_all('a'):
        url = user.get('href')
        if url is not None:
            try:
                link_set.add(url)
            except TypeError:
                print(url,'is causing TypeError')
        else: pass
    return link_set

def urlparser(url):
    if url is None:
        return None
    if url.find('google') > 0:
        return None
    try:
        pattern = '.*?http[s]{0,1}://[w.]{0,4}([\w\W\d]{1,}?)\.ai.*'
        website= re.findall(pattern, url)[0]
    except IndexError:
        website = None
    return website


def getRecorded():
    try:        
        file= open('D:/AI/'+fname,'r')
        tset = set()
        for address in file.readlines():
            website = urlparser(address)
            if website is not None:
                tset.add(website)
        file.close()
    except Exception: pass
    return tset

def getLinks():
    linkList = open('D:/AI/'+fname, 'a',buffering=1)
    ll = getRecorded()
    dupSites = 0
    newSitesAdded = 0
    pageSitesAdded = 0
    
    for pageNum in range(0,100,1):
        pageMisses = 0
        pageSitesAdded = 0
        dupSites = 0
        print('******************PAGE %d***********************'%pageNum)
        url = 'https://www.google.com/search?q=site:*.ai&start='+str(pageNum*10)
        _, soup = download(url)
        linkSet = linkExtraction(soup)
        if linkSet is None:
            print('No links were fetched;')
        else:
            for link in linkSet:
                website = urlparser(link)
                if website is not None:
                    if website in ll:
                       # print('DUP:%s'%website)
                        dupSites += 1
                    else:
                        newSitesAdded += 1
                        pageSitesAdded += 1
                        ll.add(website)
                        print('New:', website)
                        linkList.write('https://www.%s.ai'%website)
                        linkList.write('\n')
                else:
                    pass
        if pageSitesAdded == 0:
            pageMisses += 1
        else:
            pageMisses = 0
            
       
    print('Jai Google!!! New sites:%d\n Dups:%d'%(newSitesAdded,dupSites))
    linkList.close()
    return ll

import time
st = time.time()
fname='google.txt'
getLinks()
print('Time taken:%d seconds'%(time.time() - st))
