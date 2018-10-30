# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 16:32:34 2018

@author: kkonakan
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 20:41:55 2018

@author: kkonakan
"""

import urllib.request as ureq
import bs4
import re

path = 'D:/AI/DataSet/'


def download(url):
    soup = None
    html = None
    #req = Request(url, headers={'User-agent':'Mozilla/5.0'})
    try:
        html = ureq.urlopen(url).read()
        soup = bs4.BeautifulSoup(html,'lxml')
    except Exception:
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
    try:
        pattern = 'http[s]{0,1}://[w.]{0,4}([\w\W\d]{1,})\.*\.ai'
        website= re.findall(pattern, url)[0]
        if website.find('yahoo') > 0: # Yahoo search query should nt be recorded
            website = None
    except IndexError:
        website = None
    return website


def getRecorded():
    file= open('D:/AI/'+fname,'r')
    tset = set()
    for address in file.readlines():
        website = urlparser(address)
        if website is not None:
            tset.add(website)
    file.close()
    return tset


def getLinks(st_pnum, end_pnum):
    linkList = open('D:/AI/'+fname, 'a')
    ll = getRecorded()
    newSitesAdded = 0
    pageMisses = 0
    for pageNum in range(st_pnum,end_pnum+1):
        pageSitesAdded = 0
        dupSites = 0
        print('******************PAGE %d***********************'%pageNum)
        siteNum = pageNum * 10 + 1
        url='https://in.search.yahoo.com/search?p=site%3Aai&ei=UTF-8&fr=yfp-t&fp=1&b='+str(siteNum)+'&pz=10&bct=0&xargs=0'
        _, soup = download(url)
        linkSet = linkExtraction(soup)
        
        for link in linkSet:
            website = urlparser(link)
            if website is not None:
                if website in ll: 
                    dupSites += 1
                else:
                    newSitesAdded += 1
                    pageSitesAdded += 1
                    print('New:', website)
                    ll.add(website)
                    linkList.write(link)
                    linkList.write('\n')
            else:
                pass
        if pageSitesAdded == 0:
            pageMisses += 1
        if pageSitesAdded == 0 and pageMisses > 2: 
            # Breaking out of the loop when no more new sites are available
            print('No more new sites found... Hence breaking out at Page %d'%pageNum )
            break
        else:
            print('%d sites (%d dups) added from page %d'%(pageSitesAdded,dupSites,pageNum))
    print('Total number of sites added:',newSitesAdded)
    linkList.close()
    print('Yahoo!!! %d sites added (%d skipped) to the list'%(newSitesAdded, dupSites))
    return ll

import time
st = time.time()
try:
    fname = 'Final.txt'
    getLinks(0,1000)
except Exception: 
    pass
finally:
    print('Time taken:%d seconds'%(time.time() - st))
