# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 16:28:07 2018

@author: kkonakan
"""

import urllib.request as ureq
import bs4
import re
import threading
import time

class ThreadScraper(threading.Thread):
    def __init__(self, search_engine, ):
        threading.Thread.__init__(self)
        self.search_engine = search_engine
        fname = search_engine + '_links_'+'%s.txt'
        self.linkFile = 'D:/AI/'+fname
        self.DOMAIN = ''
        self.links_fetched_so_far = 0 
            
    def download(self, url):
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
    
    def linkExtraction(self, soup):
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
    
    def urlparser(self, url):
        try:
            pattern = 'http[s]{0,1}://[w.]{0,4}([\w\W\d]{1,})\.*\.%s'%self.DOMAIN
            website= re.findall(pattern, url)[0]
            if (website.find('yahoo') > 0 or website.find('bing') > 0): # Yahoo search query should'nt be recorded
                website = None
        except IndexError:
            website = None
        return website
    
    def getRecorded(self):
        file= open(self.linkFile,'r')
        tset = set()
        for address in file.readlines():
            website = self.urlparser(address)
            if website is not None:
                tset.add(website)
        file.close()
        return tset
    
    def filterBaiduLinks(self, addr):
        website= None
        for item in addr.split('www'):
            if (item.find('ai') != -1 and item.find('baidu') == -1 and item.find('container') == -1):
                pattern = '[w.]{0,4}([\w\W\d]{1,30})\.%s.*'%self.DOMAIN
                if (re.match(pattern, item)):
                    website = re.findall(pattern,item)[0]
        return website
    
    def getLinks(self, st_pnum, end_pnum, step, search_engine):
        
        print('SEARCH ENGINE REQ:', search_engine)
        linkList = open(self.linkFile, 'a')
        
        ll = self.getRecorded()
        print('Completed Reading the linkFile, retrieved %d links'%len(ll))
        
        newSitesAdded = 0
        pageMisses = 0
        totalDups = 0
        if search_engine == 'bing':
            print('bing')
            base_url = 'https://www.bing.com/search?q=site%3A'+self.DOMAIN+'&first='
            print(base_url)
            url = base_url+'0'
            print('URL',url)
        elif(search_engine == 'yahoo'):
            base_url = 'https://in.search.yahoo.com/search?p=site%3A'+\
            '%s&ei=UTF-8&fr=yfp-t&fp=1&b=%d&pz=10&bct=0&xargs=0'
            url = base_url%(self.DOMAIN,0)
        elif(search_engine == 'baidu'):
            base_url = 'https://www.baidu.com/s?wd=site%3A'+'%s&pn=%d'
            url = base_url%(self.DOMAIN,0)
        else:
            url = None
        print('URL:',url)
        print(st_pnum, end_pnum, step)
        for pageNum in range(st_pnum,end_pnum, step):
            pageSitesAdded = 0
            dupSites = 0
            print('******************PAGE %d***********************'%(pageNum))
            siteNum = pageNum * 10 + 1
            url = base_url+ str(siteNum)
            _, soup = self.download(url)
            linkSet = self.linkExtraction(soup)
            if linkSet is None:
                continue
            for link in linkSet:
                website = self.urlparser(link)
                if link.find('baidu') > -1:
                    website = self.filterBaiduLinks(link)
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
                print('%s: %d sites added \n'%(self.search_engine, pageSitesAdded))
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
    
    def run(self):
        #search_engine = self.search_engine
        st = time.time()
        DOMAIN = ''
        doms_to_crawl=['in','nl']
        for DOMAIN in doms_to_crawl:
            
            self.DOMAIN= DOMAIN
            self.links_fetched_so_far = 0
            print('CURRENT DOMAIN : ', DOMAIN)
            sl_seconds = 2
            en_pnum = 0
            print('DOMAIN:',DOMAIN)
            step = 1
            tot_pages = 0
            for st_pnum in range(0,20):
                    if(st_pnum != 0 and st_pnum%100 == 0):
                        step += 5            
                    en_pnum = st_pnum + 100   
                    ladded = self.getLinks(st_pnum, en_pnum, step, self.search_engine)
                    self.links_fetched_so_far += len(ladded)
                    print('Links fetched so far:',self.links_fetched_so_far)
                    print('Sleeping for %d seconds'%sl_seconds)
                    time.sleep(sl_seconds)
            try:pass
                
            except Exception: 
                pass
            finally:
                print('Total pages: %d'%tot_pages)
                print('Time taken:%d seconds'%(time.time() - st))
                
#for search_engine in ['bing','baidu','yahoo']:
current = ThreadScraper('bing')
current.start()