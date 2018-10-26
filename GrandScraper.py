# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 10:32:33 2018

@author: kkonakan
"""

import urllib.request as ureq
import bs4
import re
def download(url):
    soup = None
    html = None
    if url.find('baidu') > 0:
        url = ureq.Request(url, headers={'User-agent':'Mozilla/5.0'})
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
        if (website.find('yahoo') > 0 or website.find('bing') > 0): # Yahoo search query should'nt be recorded
            website = None
    except IndexError:
        website = None
    return website

def getRecorded():
    file= open(linkFile,'r')
    tset = set()
    for address in file.readlines():
        website = urlparser(address)
        if website is not None:
            tset.add(website)
    file.close()
    return tset

def filterBaiduLinks(addr):
    website= None
    for item in addr.split('www'):
        if (item.find('ai') != -1 and item.find('baidu') == -1 and item.find('container') == -1):
            pattern = '[w.]{0,4}([\w\W\d]{1,30})\.ai.*'
            if (re.match(pattern, item)):
                website = re.findall(pattern,item)[0]
    return website

def getLinks(st_pnum, end_pnum):
    linkList = open(linkFile, 'a')
    ll = getRecorded()
    newSitesAdded = 0
    pageMisses = 0
    totalDups = 0
    for pageNum in range(st_pnum,end_pnum+1):
        urls = []
        pageSitesAdded = 0
        dupSites = 0
       # print('******************PAGE %d***********************'%(pageNum+st_pnum))
        siteNum = pageNum * 10 + 1
        urls.append('https://in.search.yahoo.com/search?p=site%3Aai&ei=UTF-8&fr=yfp-t&fp=1&b='+str(siteNum)+'&pz=10&bct=0&xargs=0')
        urls.append('https://www.bing.com/search?q=site%3aai&qs=n&lf=1&sp=-1&pq=site%3aai&sc=1-7&sk=&cvid=E51964C6ABF84C34A3FE347FE1AC9789&first='+str(siteNum)+'&FORM=PORE')
        siteNum -= 1
        urls.append('https://www.baidu.com/s?wd=site%3Aai&pn='+str(siteNum)+'&oq=site%3Aai&ie=utf-8')
        
        for url in urls:
           # searchEngine = re.findall('http[s]{0,1}://.*\.([\w\W\d]{1,})\.*\.com', url)[0]
           # print('Current SearchEngine:%s\n'%searchEngine.upper())
            
            _, soup = download(url)
            linkSet = linkExtraction(soup)
            
            for link in linkSet:
                website = urlparser(link)
                if link.find('baidu') > -1:
                    website = filterBaiduLinks(link)
                if website is not None:
                    if website in ll: 
                        #print(website,'is a dup')
                        dupSites += 1
                    else:
                        newSitesAdded += 1
                        pageSitesAdded += 1
                        #print('*********New:', website)
                        ll.add(website)
                        linkList.write(link)
                        linkList.write('\n')
                else:
                    pass
            totalDups += dupSites
        if pageSitesAdded == 0:
            pageMisses += 1
        elif pageSitesAdded > 0:
            pageMisses = 0
            '''
        if pageSitesAdded == 0 and pageMisses > 10: 
            # Breaking out of the loop when no more new sites are available
            print('No more new sites found since %d pages... Hence breaking out at Page %d'%(pageMisses,pageNum) )
            break
        else:
            print('%d sites (%d dups) added from page %d'%(pageSitesAdded,dupSites,pageNum))
            '''
    #print('Returning with %d new sites and %d dups:'%(newSitesAdded,totalDups))
    linkList.close()
    print('Hurray!!! %d sites added (%d skipped) to the list'%(newSitesAdded, totalDups))
    return ll

import time
st = time.time()

linkFile = 'D:/AI/linksv1.txt'
try:
    step = 100
    for st_pnum in range(0,1001,step):
        en_pnum = st_pnum + step   
        print('Trying from %d to %d pages'%(st_pnum,en_pnum))
        getLinks(st_pnum,en_pnum)
        print('Sleeping for 30 minutes')
        time.sleep(1800)
except Exception: 
    pass
finally:
    print('Time taken:%d seconds'%(time.time() - st))
