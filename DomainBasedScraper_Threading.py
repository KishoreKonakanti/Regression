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
    
    def __init__(self, search_engine):
        global logFile
        threading.Thread.__init__(self)
        self.search_engine = search_engine
        self.linkFile = 'D:/AI/'
        self.DOMAIN = ''
        self.links_fetched_so_far = 0 
        self.loaded = False
        self.linkSet = None
        self.lock = threading.Lock()
            
    def download(self, url):
        soup = None
        html = None
        if url.find('baidu') > 0:
            url = ureq.Request(url, headers={'User-agent':'Mozilla/5.0'})
        try:
            html = ureq.urlopen(url, timeout=30).read()
            soup = bs4.BeautifulSoup(html,'lxml')
            ##print(html, soup.contents)
            soup.encode('utf-8')
        except Exception:
            print(self.name+'=> '+url,' site is not allowing bots')
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
                    print(self.name+'=> '+url,'is causing TypeError')
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
    
    def prMsg(self, message):
        print('%s (%s) => %s'%(self.name.upper(), self.DOMAIN, message))
        
    def logWrite(self, message):
        
        if logFile is None:
            return None
            
        message = '%s (%s) => %s'%(self.name.upper(), self.DOMAIN, message)
        self.lock.acquire()
        logFile.write(message)
        logFile.write('\n')
        self.lock.release()
    
    def getRecorded(self):
        
        file= open(self.linkFile,'r', encoding='utf-8')
        tset = set()
        for address in file.readlines():
            website = self.urlparser(address)
            if website is not None:
                tset.add(website)
                
        file.close()
        
        self.logWrite('Loaded %d links from %s file'%(len(tset), self.DOMAIN))
        
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
        
        #print(self.name+'=> '+'SEARCH ENGINE REQ:', search_engine)
        linkList = open(self.linkFile, 'a', encoding='utf-8')
        if self.linkSet is None:
            self.linkSet = self.getRecorded()
            #print('Completed Reading the linkFile, retrieved %d links'%len(self.linkSet))
        
        newSitesAdded = 0
        pageMisses = 0
        totalDups = 0
        base_url = ''
        base_url_2 = '' # Used only with YAHOO
        if search_engine == 'bing':
            base_url = 'https://www.bing.com/search?q=site%3A'+self.DOMAIN+'&first='
            url = base_url+'0'
        elif(search_engine == 'yahoo'):
            base_url = 'https://in.search.yahoo.com/search?p=site%3A'+self.DOMAIN+'&ei=UTF-8&fr=yfp-t&fp=1&b='
            base_url_2 = '&pz=10&bct=0&xargs=0'
            url = base_url + '0' + base_url_2
        elif(search_engine == 'baidu'):
            base_url = 'https://www.baidu.com/s?wd=site%3A'+self.DOMAIN+'%s&pn=%d'
            url = base_url + '0'
        else:
            url = None
        ##print('BASE_URL:', url)
        for pageNum in range(st_pnum, end_pnum, step):
            ##print(pageNum,' is the CURRENT page')
            pageSitesAdded = 0
            dupSites = 0
            print('******************PAGE %d***********************'%(pageNum+st_pnum))
            siteNum = pageNum * 10
            
            url = base_url+ str(siteNum)
            
            if self.search_engine is 'yahoo':
                url += base_url_2
                
            _, soup = self.download(url)
       #     ##print('=====================Link Set:',self.name,'',soup)
            
            linkSet = self.linkExtraction(soup)
        #    #print('=====================Link Set:',self.name+linkSet)
            
            if linkSet is None:
                continue
            for link in linkSet:
                website = self.urlparser(link)
                if link.find('baidu') > -1:
                    website = self.filterBaiduLinks(link)
                if website is not None:
                    if website in self.linkSet: 
                        ##print(website,'is a dup')
                        dupSites += 1
                    else:
                        newSitesAdded += 1
                        pageSitesAdded += 1
                        self.linkSet.add(website)
                        linkList.write(link)
                        linkList.write('\n')
                else:
                    pass
            
                totalDups += dupSites
            #self.prMsg('%s: %d sites added \n'%(self.search_engine, pageSitesAdded))
            if pageSitesAdded == 0:
                pageMisses += 1
            elif pageSitesAdded > 0:
                pageMisses = 0
        linkList.close()
        
        return  pageSitesAdded
    
    def run(self):
        st = time.time()
        DOMAIN = ''
        
        doms_to_crawl=['io','ml','ai']
        
        for DOMAIN in doms_to_crawl:
            self.DOMAIN= DOMAIN
            self.linkFile = 'D:/AI/%s_links_%s.txt'%(self.search_engine, self.DOMAIN)
            self.links_fetched_so_far = 0
            self.linkSet = None
            sl_seconds = 10
            en_pnum = 0
            step = 1
            tot_pages = 0
            for st_pnum in range(0,1000,100):
                    if(st_pnum != 0 and st_pnum%100 == 0):
                        step += 10       
                    en_pnum = st_pnum + 100
                    tot_pages += int((en_pnum - st_pnum +1)/step)    
                    
                    psadded  = self.getLinks(st_pnum, en_pnum, step, self.search_engine)
                    
                    self.prMsg('%d sites added'%psadded)
                    self.prMsg('Sleeping for %d seconds'%sl_seconds)
                    time.sleep(sl_seconds)

            self.logWrite('%d new Links added for domain ** %s **'%(len(self.linkSet), DOMAIN.upper()))
                    
        #print('Link File:', self.linkFile)
        #print('Time taken:%d seconds\n'%(time.time() - st))

st = time.time()
search_threads = []        

logFile = open('D:/AI/log.txt','a')
logFile.write('****************************************************')
logFile.write('\n')
logFile.write('Starting at '+time.asctime())
logFile.write('\n')

for search_engine in ['bing','baidu','yahoo']:
    current = ThreadScraper(search_engine)
    current.setName(search_engine)
    search_threads.append(current)
    #print('Thread started for search engine %s\n\n'%(current.name))
    current.start()
    time.sleep(1)

# Cleanup code:
    
for thread in search_threads:
    thread.join()
    
logFile.close()

print('DONE')
print('Time taken:%d seconds\n'%(time.time() - st))
