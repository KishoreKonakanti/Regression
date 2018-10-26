# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 17:16:04 2018

@author: kkonakan
"""


import urllib.request as ureq
import bs4
import re

path = 'D:/AI/DataSet/'


def download(url):
    soup = None
    html = None
    req = ureq.Request(url, headers={'User-agent':'Mozilla/5.0'})
    try:
        html = ureq.urlopen(req).read()
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
            #print(url)
            try:
                link_set.add(url)
            except TypeError:
                print(url,'is causing TypeError')
        else: pass
    return link_set


def clean():
    try:
        scrapeList.close()
    except Exception:
        pass
    return

def urlparser(url):
    import re
    try:
        pattern = 'http[s]{0,1}://[w.]{0,4}([\w\W\d]{1,})\.*\.ai'
        website= re.findall(pattern, url)[0]
        if website.find('baidu') > 0: # Yahoo search query should nt be recorded
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

def processSite(addr):
    website= None
    for item in addr.split('www'):
        if (item.find('ai') != -1 and item.find('baidu') == -1 and item.find('container') == -1):
            pattern = '[w.]{0,4}([\w\W\d]{1,30})\.ai.*'
            if (re.match(pattern, item)):
                website = re.findall(pattern,item)[0]
    return website

def getLinks(st_pnum, end_pnum):
    linkList = open('D:/AI/'+fname, 'a')
    ll = getRecorded()
    newSitesAdded = 0
    dupSite = 0
    pageMisses = 0
    for pageNum in range(st_pnum,end_pnum+1):
        pageSitesAdded = 0
        dupSites = 0

        print('******************PAGE %d***********************'%pageNum)
        siteNum = pageNum * 10
        url='https://www.baidu.com/s?wd=site%3Aai&pn='+str(siteNum)+'&oq=site%3Aai&ie=utf-8'
        html, soup = download(url)
        linkSet = str(html).split('www')
        for link in linkSet:
            website = processSite(link)
            link = 'http://www.%s.ai'%website
            if website is not None:
                if website in ll: 
                    dupSite += 1
                else:
                    newSitesAdded += 1
                    pageSitesAdded += 1
                    print('New:', website)
                    ll.add(website)
                    linkList.write(link)
                    linkList.write('\n')
        if pageSitesAdded == 0:
            pageMisses += 1
        if pageSitesAdded == 0 and pageMisses > 2: 
            # Breaking out of the loop when no more new sites are available
            print('No more new sites found... Hence breaking out at Page %d'%pageNum )
            break
        else:
            print('%d sites (%d dups) added from page %d'%(pageSitesAdded,dupSites,pageNum))
        if pageSitesAdded == 0: # Breaking out of the loop when no more new sites are available
            print('No more new sites found... Hence breaking out at Page %d'%pageNum )
            break
        else:
            print('%d sites (%d dups) added from page %d'%(pageSitesAdded,dupSites,pageNum))

    linkList.close()
    print('Adieu !!! %d sites added (%d skipped) to the list'%(newSitesAdded, dupSite))
    return ll

import time
st = time.time()
fname = 'Final.txt'
rc = re.compile('http[s]{0,1}://[w.]{0,4}([\w\W\d]{1,})\.*\.ai')
scrapeList = None
getLinks(0,1000)
clean()
print('Time taken:%d seconds'%(time.time() - st))
