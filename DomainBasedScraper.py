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
        html = ureq.urlopen(url, timeout=30).read()
        soup = bs4.BeautifulSoup(html,'lxml')
    except Exception:
        print(url.get_full_url())
        print(url,' site is not allowing bots')
    return html,soup

def linkExtraction(soup):
    if soup is None:
        return None
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
        pattern = 'http[s]{0,1}://[w.]{0,4}([\w\W\d]{1,})\.*\.%s'%DOMAIN
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
            pattern = '[w.]{0,4}([\w\W\d]{1,30})\.%s.*'%DOMAIN
            if (re.match(pattern, item)):
                website = re.findall(pattern,item)[0]
    return website

def getLinks(st_pnum, end_pnum, step):
    linkList = open(linkFile, 'a')
    
    ll = getRecorded()
    print('Completed Reading the linkFile, retrieved %d links'%len(ll))
    
    newSitesAdded = 0
    pageMisses = 0
    totalDups = 0
    for pageNum in range(st_pnum,end_pnum, step):
        urls = []
        pageSitesAdded = 0
        dupSites = 0
        #print('******************PAGE %d***********************'%(pageNum))
        siteNum = pageNum * 10 + 1
        urls.append('https://in.search.yahoo.com/search?p=site%3A'+DOMAIN+'&ei=UTF-8&fr=yfp-t&fp=1&b='+str(siteNum)+'&pz=10&bct=0&xargs=0')
        urls.append('https://www.bing.com/search?q=site%3a'+DOMAIN+'&qs=n&lf=1&sp=-1&pq=site%3aai&sc=1-7&sk=&cvid=E51964C6ABF84C34A3FE347FE1AC9789&first='+str(siteNum)+'&FORM=PORE')
        siteNum -= 1
        urls.append('https://www.baidu.com/s?wd=site%3A'+DOMAIN+'&pn='+str(siteNum)+'&oq=site%3Aai&ie=utf-8')
        
        for url in urls:
            
            searchEngine = re.findall('http[s]{0,1}://.*\.([\w\W\d]{1,})\.*\.com', url)[0].upper()
            
            _, soup = download(url)
            linkSet = linkExtraction(soup)
            if linkSet is None:
                continue
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
            print('%s: %d sites added \n'%(searchEngine, pageSitesAdded))
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
    #print('%d sites added (%d skipped) to the list'%(newSitesAdded, totalDups))
    return ll

import time
st = time.time()
DOMAIN = ''
doms_to_crawl=['io','ml']
for DOMAIN in doms_to_crawl:
    links_fetched_so_far = 0
    print('CURRENT DOMAIN : ', DOMAIN)
    sl_seconds = 30
    en_pnum = 0
    print('DOMAIN:',DOMAIN)
    linkFile = 'D:/AI/%s_links.txt'%DOMAIN
    step = 1
    tot_pages = 0
    try:
        for st_pnum in range(0,500,50):
            if(st_pnum != 0 and st_pnum%100 == 0):
                step += 5            
            en_pnum = st_pnum + 100   
            links_fetched_so_far += len(getLinks(st_pnum, en_pnum, step))
            tot_pages += int((en_pnum - st_pnum + 1)/step)
            print('Links fetched so far:',links_fetched_so_far)
            print('Sleeping for %d seconds'%sl_seconds)
            time.sleep(sl_seconds)
    except Exception: 
        pass
    finally:
        print('Total pages: %d'%tot_pages)
        print('Time taken:%d seconds'%(time.time() - st))
