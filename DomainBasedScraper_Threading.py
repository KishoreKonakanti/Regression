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
        self.linkFileName = '' # This will be set in getLinks()
        self.DOMAIN = ''
        self.links_fetched_so_far = 0 
        self.linkSet = None   # Loaded in getRecorder()
        self.linkFile = None # Set in run()
        try:
            self.lock = threading.Lock()
        except threading.ThreadError as the:
            print('Unable to acquire a lock')
            print('Full trace: %s'%the)
        
            
    def download(self, url):
        soup = None
        html = None
        req = None
        if url.find('google') > 0: 
            req = ureq.Request(url, headers={'User-agent':'Firefox/2.0.0.11'})
        try:
            if req is None:
                html = ureq.urlopen(url, timeout=30).read()
            else:
                html = ureq.urlopen(req, timeout=30).read()
            soup = bs4.BeautifulSoup(html,'lxml')
            soup.encode('utf-8')
        except Exception as e:
            print(self.name+'=> '+ url)
            message='Exception %s has occurred'%e
            self.fileWrite(message,file=logFile,pr=True)
            html = None
            soup = None
            
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
            pattern = 'http[s]{0,1}://[w.]{0,4}([\w\W\d]{1,})\.*\.%s'%self.DOMAIN.lower()
            #self.pr(pattern+':::'+url)
            url = url.lower()
            currentLink= re.findall(pattern, url)[0]
            if (currentLink.find('yahoo') > 0 or currentLink.find('bing') > 0): # Yahoo search query should'nt be recorded
                currentLink = None
        except IndexError:
            currentLink = None
        return currentLink
    
    def pr(self, message):
        print('%s (%s) => %s\n'%(self.name.upper(), self.DOMAIN, message))
        

    def fileWrite(self, message, file=None, pr=False, header=True):
        if file is None: # Default writes goes to logFiles unless specified otherwise
            global logFile
            file = logFile
        if logFile is None:
            return None
        if header is True:
            message = '%s (%s) => %s'%(self.name.upper(), self.DOMAIN, message)
        else:
            message = message
            
        self.lock.acquire()
        file.write(message)
        file.write('\n')
        self.lock.release()
        if pr is True:
            print(message)
        return True
    
    def getRecorded(self):
        
        if len(linkSet_dict[self.DOMAIN]) != 0:
            #self.pr('Links already loaded for '+self.DOMAIN)
            return True
        
        try:
            self.lock.acquire()
            file= open(self.linkFileName,'r', encoding='utf-8')
            tset = set()
            for address in file.readlines():
                currentLink = self.urlparser(address)
                if currentLink is not None:
                    tset.add(currentLink)
                    
            file.close()
            linkSet_dict[self.DOMAIN] = tset
            self.lock.release()
            
            self.fileWrite('Loaded %d links from %s file'%(len(tset),self.DOMAIN), \
                           file=logFile)
        except FileNotFoundError as fe:
            print('File %s not found'%self.linkFileName)
            print('Full trace: %s'%fe)
        except AttributeError:
            return None
        
        return True
    
    def filterBaiduLinks(self, addr):
        currentLink= None
        for item in addr.split('www'):
            if (item.find('ai') != -1 and item.find('baidu') == -1 and item.find('container') == -1):
                pattern = '[w.]{0,4}([\w\W\d]{1,30})\.%s.*'%self.DOMAIN
                if (re.match(pattern, item)):
                    currentLink = re.findall(pattern,item)[0]
        return currentLink
    
    def getLinks(self, st_pnum, end_pnum, step, search_engine):
        
        #print(self.name+'=> '+'SEARCH ENGINE REQ:', search_engine)
#        linkList = open(self.linkFile, 'a', encoding='utf-8')
        if self.linkSet is None:
            self.linkSet = linkSet_dict[self.DOMAIN]
        
        newSitesAdded = 0
       # pageMisses = 0
        totalDups = 0
        base_url = ''
        base_url_2 = '' # Used only with YAHOO
        
        if search_engine == 'bing':
            base_url = 'https://www.bing.com/search?q=site%3A'+self.DOMAIN+'&first='
            url = base_url+'0'
        elif(search_engine == 'yahoo'):
            base_url = 'https://in.search.yahoo.com/search?p=site%3A'+\
                        self.DOMAIN+'&ei=UTF-8&fr=yfp-t&fp=1&b='
            base_url_2 = '&pz=10&bct=0&xargs=0'
            url = base_url + '0' + base_url_2
        elif(search_engine == 'baidu'):
            base_url = 'https://www.baidu.com/s?wd=site%3A'+self.DOMAIN+'&pn='
            url = base_url + '0'
        elif(search_engine == 'google'):
            base_url = 'https://www.google.com/search?q=site:*.'+self.DOMAIN+'&start='
            url = base_url + '0'
        else:
            url = None
            
            
        for pageNum in range(st_pnum, end_pnum, step):
            pageSitesAdded = 0
            dupSites = 0
            #self.fileWrite('******************PAGE %d***************'%(pageNum), file=logFile,pr=True)
            siteNum = pageNum * 10
            
            url = base_url+ str(siteNum)
            
            if self.search_engine is 'yahoo':
                url += base_url_2
                
            _, soup = self.download(url)
            
            if(self.search_engine.find('google') > 0):
                time.sleep(2)
                
            currLinkSet = self.linkExtraction(soup)
            #self.pr(currLinkSet)
            
            if currLinkSet is None:
                print('Nothing in the currLinkSet')
            else:
                self.linkSet = linkSet_dict[self.DOMAIN] # Load the already known links
                for link in currLinkSet:
                    currentLink = self.urlparser(link)
                    
                    if currentLink is not None:
                        if(link.find('baidu') > -1):
                            currentLink = self.filterBaiduLinks(link)
                        if currentLink in self.linkSet: 
                            #self.pr(currentLink+'is a dup')
                            dupSites += 1
                        else:
                            newSitesAdded += 1
                            pageSitesAdded += 1
                            self.linkSet.add(currentLink)
                            self.fileWrite(message=link, file=self.linkFile, header=False)                        
                    else: 
                    # Current currentLink link is None due to pattern match failure in urlparser
                        pass
                
                    totalDups += dupSites
            self.fileWrite('%d sites added from page %d to %d '%(pageSitesAdded, st_pnum, end_pnum), \
                           file=logFile)
            '''
            if pageSitesAdded == 0:
                pageMisses += 1
            elif pageSitesAdded > 0:
                pageMisses = 0
                '''
        
        return  pageSitesAdded,dupSites
    
    def run(self):
        global domain_list
        start_th = time.time()
        DOMAIN = ''
                
        for DOMAIN in domain_list:
            self.DOMAIN= DOMAIN.upper()
            self.linkFileName = 'D:/AI/%s.txt'%(self.DOMAIN)
            
            self.links_fetched_so_far = 0
            self.getRecorded() # Read the link file and close this. Link File will be 
            # opened in getLinks agains to write new links
            self.linkSet = linkSet_dict[self.DOMAIN]
            #print('Loaded links:',len(self.linkSet))
            self.linkFile = open(self.linkFileName,'a',encoding='utf-8')
            sl_seconds = 10
            en_pnum = 0
            step = 1
            tot_pages = 0
            for st_pnum in range(0,1000,100):
                    if(st_pnum != 0 and st_pnum%100 == 0):
                        step += 10   
                        if step > 50: # Atleast 2 pages must be loaded from each set
                            step = 40
                    en_pnum = st_pnum + 100
                    tot_pages += int((en_pnum - st_pnum +1)/step)   
                    
                    self.pr('Pages: %d %d %d'%(st_pnum,en_pnum,step))
                    
                    psadded,dupCnt  = self.getLinks(st_pnum, en_pnum, step, self.search_engine)
                    
                    siteCount[search_engine+'new'] += psadded
                    siteCount[search_engine+'dup'] += dupCnt
                    
                    time.sleep(sl_seconds)

            self.fileWrite('%d new Links added for domain ** %s **'%(len(self.linkSet), self.DOMAIN), file=logFile)
                    
        #print('Link File:', self.linkFile)
        print('Time taken for thread %s:%d seconds\n'%(self.name,(time.time() - start_th)))
        

start_time = time.time()
search_threads = []        
linkSet_dict={}
siteCount= {}
domain_list=['io','ml','ai']
search_engines = ['bing','yahoo','google']
#search_engines=['google']

logFile = open('D:/AI/log.txt','a', buffering=1)
logFile.write('****************************************************')
logFile.write('\n')
logFile.write('Starting at '+time.asctime())
logFile.write('\n')

for domain in domain_list:
    linkSet_dict[domain.upper()] = set([])

for search_engine in search_engines:
    siteCount[search_engine+'new'] = 0
    siteCount[search_engine+'dup'] = 0
    current = ThreadScraper(search_engine)
    current.setName(search_engine)
    search_threads.append(current)
    print('Thread started for search engine %s\n\n'%(current.name))
    current.start()
    time.sleep(120)

# Cleanup code:
    
for thread in search_threads:
    print(('Waiting for %s to join'%thread.name).upper())
    thread.join()

print('DONE')
print('Site stats',siteCount)
print('Time taken:%d seconds\n'%(time.time() - start_time))
