# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 16:11:15 2018

@author: kkonakan
"""


from urllib import request as ureq
import bs4
import re
from numpy import NaN
import os
import csv
import time
import threading

class FetchDetails(threading.Thread):
    
    def __init__(self, fileName, writer, linkCount, linkBase, csvOutputFile):
        super(FetchDetails, self).__init__()
        self.inFile = 'D:/AI/%s.txt'%fileName  # Input links file
        self.DOMAIN = fileName
        self.writer = writer # CSV output writer
        self.crawledList = set()
        self.log = 0 # No log
        self.lock = threading.Lock()
        self.baseName = None
        self.linkBase = linkBase
        self.linkCount = linkCount
        self.skipLinks = skipLinks
        self.csvOutputFile = csvOutputFile
        
    def getAlexaRank(self,url):
        if self.log == 1:
            print('getAlexaRank')
        base_url = 'https://www.alexa.com/siteinfo/'
        comp_url = base_url+url
        html,_ = self.download(comp_url)
        html = str(html)
        rank = None
        try:
            rank = re.findall('.*global\":([\d].*?)}.*',html)[0]
            return rank
        except Exception:
            return None
    
    def getCountryReg(self,url):
        if self.log == 1:
            print('getCountryReg')
        '''whois limits 5 reqs per day'''
        return None
        addr = 'http://whois.DOMAINtools.com/%s'%url
        _,WS = self.download(addr)
        lls = []
        for div in WS.find_all('div'):
            if(div.get('id') == 'stats'):
                for ch in div.findChildren('td'):
                    lls.append(ch.contents)
        ind = lls.index(['Registrant Country'])
        return lls[ind+1] or None
    
    def getHostCountry(self,url):
        if self.log == 1:
            print('getHostCountry')
        addr='http://data.alexa.com/data?cli=10&url=%s'%url
        _,S = self.download(addr)
        country = None
        for i in S.find_all('country'):
            country = re.findall(r'.*?name=\"(.*?)\".*', str(i))[0]
        return country
    
    def isUsingJS(self,soup):
        if self.log == 1:
            print('isUsingJS')
        t = soup.find_all('script')
        if len(t) == 0:
            return 0
        else:
            return 1
    
    def isUsingCSS(self,html):
        if self.log == 1:
            print('isUsingCSS')
        H = str(html)
        if(str(H).find('css') > 0):
            return 1
        else:
            return 0
    
    def saveHTML(self,url, content):
        return True # Bypassing saveHTML
        '''
            Saves the file to the disk and returns size of the html file in KB
        '''
        if self.log == 1:
            print('saveHTML')
        if content is None:
            print('THERE IS NOTHING TO WRITE, RECEIVED NONE')
            return -1
        
        global path
        fname = None
        size = 0
        
        try:
            self.lock.acquire()
            #baseName = self.getBaseName(url)
            fname = 'D:/AI/Dataset/%s/%s_%s.html'%(self.DOMAIN.upper(),\
                                                   self.baseName, self.DOMAIN)
            print(fname,' is name of the file')
            ufile = open(fname, 'w')
            ufile.writelines(str(content))
            ufile.close()
            self.lock.release()
            size= round(os.path.getsize(fname)/1024)
        except Exception as e:
            print('Error occured during %s saving: %s'%(url,e))
        if self.log == 1:
            print('Returning successfully from saveHTML')
        return size
    
    def download(self,url):
        if self.log == 1:
            self.pr('download requested for ', url)
        soup = None
        html = None
        self.lock.acquire()
        req = ureq.Request(url, headers={'User-agent':'Mozilla/5.0'})
        try:
            html = ureq.urlopen(req, timeout=30).read()
            soup = bs4.BeautifulSoup(html,'lxml')
        except Exception as e:
            print('DOWNLOAD:',url,' site is not allowing bots with stack as ',e)
        #self.pr('Returning html,soup')
        self.lock.release()
        return html,soup
    
    def fillNans(self,siteDetails):
        if self.log == 1:
            print('fillNans')
        global props
        for prop in props:
            if(siteDetails.get(prop,-12345) == -12345):
                siteDetails[prop] = NaN
            else: pass
        return 0
    
    def flatten(self, multiLine):
        if multiLine is None:
            return None
        if(len(multiLine) == 1):
            return multiLine
        retL = ''
        for l in multiLine:
           retL = '%s %s'%(retL, l)
        return retL
    
    def populateSiteDetails(self,url):
        if self.log == 1:
            print('populate')
        '''
            Retrieves site Details
            Saves the html content to disk for later processing
        '''
        
        html = None
        contentSoup = None
        siteDetails= {}
        html,contentSoup = self.download(url)
        if contentSoup is not None and contentSoup.title is not None:
            #print('Content Soup is not NONE:', contentSoup.title)
            siteDetails['url'] = url.strip()
            siteDetails['numLinks'] = len(contentSoup.find_all('a'))
            siteDetails['title'] = self.flatten(contentSoup.title.string)
            siteDetails['hostedIn'] = self.getHostCountry(url)
            #siteDetails['RegIn'] = getCountryReg(url)
            siteDetails['AlexaRank'] = self.getAlexaRank(url)
            siteDetails['CSS'] = self.isUsingCSS(html)
            siteDetails['JS'] = self.isUsingJS(contentSoup)
            siteDetails['size'] = self.saveHTML(url, html)
            for metaTags in contentSoup.find_all('meta'):
                #print('Populating Tags')
                attrs = metaTags.attrs
                if ('name' in attrs.keys() and 'content' in attrs.keys()): # Reading meta tags
                    name = attrs['name']
                    dets = attrs['content']
                    if (name == 'title'):
                        siteDetails['title'] = self.flatten(dets)
                    elif (name == 'description' ):
                        siteDetails['descr'] = self.flatten(dets)
                    elif(name == 'keywords'):
                        siteDetails['kwords'] = self.flatten(dets)
                    else:
                        pass
                else: pass
        else: 
            siteDetails['url'] = url
            siteDetails['title']= self.getBaseName(url).upper()
        self.crawledList.add(url)
        return siteDetails
            
    def getBaseName(self,url):
        #print('Incoming ',url)
        import re
        pattern = '[whtps:/.]{0,12}([\w\W\d\.]{1,})\.*\.%s'%self.DOMAIN.lower()
        baseName= re.findall(pattern, url)[0]
        #print('URL:%s->%s'%(url,baseName))
        return baseName
    
    def transform(self,link):
        if link is None or link == '' :
            return None
        if self.log == 1:
            print('Incoming link:',link)
        exact_pattern = 'http[s]{0,1}://[w.]{0,4}[\w\W\d]*?\.%s$'%self.DOMAIN.lower()
        extra_pattern = 'http[s]{0,1}://[w.]{0,4}([\w\W\d]*)?\.%s\/.*$'%self.DOMAIN.lower()
        base_url = None
    
        if(re.match(exact_pattern, link)):
            self.baseName = re.findall(extra_pattern,link)[0]
            base_url = link
        elif(re.match(extra_pattern, link)):
            self.baseName = re.findall(extra_pattern,link)[0]
            base_url = 'https://www.%s.%s'%(self.baseName,self.DOMAIN.lower())
        else:pass
    
        if base_url is None:
            self.pr('INVALID Link:%s'%link)
    #    else:
     #       self.pr('Returning %s'%base_url)
        return base_url
    
    def pr(self,message):
        print('%s => %s'%(self.name, message))
        return None
        
    
    def run(self):
        cnt = 0
        global start_time
        
        self.linkCount = len(linkBase)
       
        for link in self.linkBase:
            #print('HERE')
            
            self.pr('Current Site# %d / %d: %s'%(cnt,self.linkCount,link ))
            cnt += 1

            siteDets = self.populateSiteDetails(link)
            self.pr('Length of sitedetails: %d'%len(siteDets))
            
            self.lock.acquire()
            # WRITE SITEDETAILS AND INCREMENT THE NUMBER OF POPULATED SITES BY 1
            self.writer.writerow(siteDets)
            
            populateCount[self.name] += 1
            self.lock.release()
            
        global completedThreadCount
        completedThreadCount += 1
        self.pr('**********************Time for this thread to complete: %d seconds'%(time.time()-start_time))
    def getLineCount(fname):
        with open(fname) as foo:
            return len(foo.readlines())
    


# GLOBALS
def getLineCount(fname):
        with open(fname) as foo:
            return len(foo.readlines())
            

props = ['url','title','descr','numLinks','kwords','AlexaRank','hostedIn','CSS',
         'JS','size']
thread_set = []
DOMAIN_list = ['IO']
populateCount = {}
completedThreadCount = 0
crawledBase = set()
'''
if os.path.isfile('D:/AI/Dataset/IO.csv'):
    df = pd.read_csv('D:/AI/Dataset/IO.csv', encoding='ISO-8859-1')
    urls = df['url'].unique()
    crawledBase = set(urls)
print('LENGTH OF CRAWLED BASE:',len(crawledBase))
del df
'''
try:
    start_time = time.time()
    path = 'D:/AI/DataSet/'
    
    
    for DOMAIN in DOMAIN_list:
        csvOutputFile='%s/%s.csv'%(path, DOMAIN)
        fname = 'D:/AI/%s.txt'%DOMAIN
        # Based on the linecount, start a new thread for every 100 links
        #   Easier to start but harder to write to the csvOutputFile.csv        
        allLinks = []
        
        with open(fname) as inFile:
            for link in inFile.readlines():
                allLinks.append(link.strip())
        
        
        csvfile=open(csvOutputFile, 'w', encoding='utf-8-sig', buffering=1)
        writer = csv.DictWriter(csvfile, props, restval=NaN)
        
        numLinksPerThread = 50
        sl_seconds = 60
        availableLinkCount = getLineCount(fname)
        
        if availableLinkCount%numLinksPerThread == 0:
            threadCount = availableLinkCount//numLinksPerThread
        else:
            threadCount = (availableLinkCount//numLinksPerThread) + 1
        
        print('NUMBER OF THREADS WILL BE %d'%threadCount)
        time.sleep(10)
        # Use skipLinks in run method to spawn a thread for each 100 links. 
        # For each domain, number of threads will be ( linkCount%100 ) +1
        
        skipLinks = 0
        threadNum = 0
        st = time.time()
        
        writer.writeheader()
        
        while threadNum < threadCount:
            
            threadName = '%s: %d'%(DOMAIN, threadNum)
            skipLinks = numLinksPerThread*threadNum    
            linkBase = allLinks[skipLinks:skipLinks+numLinksPerThread]
            #print('Time: %d'%(time.time() - st))
            print('\nThread %d: Skipping first %d links'%(threadNum,skipLinks))
            threadNum += 1
            current = FetchDetails(DOMAIN, writer, 100, linkBase, csvOutputFile)
            current.setName(threadName)
            populateCount[threadName] = 0
            thread_set.append(current)
            print('\nStarting a thread for %s'%(DOMAIN))
            current.start()        
            skipLinks += 100
            time.sleep(sl_seconds)  
        
        # Last thread if numLinks > 1
        if availableLinkCount%100 != 0:
            threadNum -= 1
        if threadCount > threadNum:
            linkBase = allLinks[skipLinks:]
            print('Thread %d: Remaining %d links'%len(linkBase))
            current = FetchDetails(DOMAIN, writer, len(linkBase), linkBase)
            current.name = '%s-LAST'%DOMAIN
            thread_set.append(current)
            current.start()
    
    for thread in thread_set:
         print('Waiting for thread %s to join'%thread.name)
         thread.join(timeout=7200)
         print('NUMBER OF LINKS COVERED ARE',populateCount)
         if(thread.is_alive()):
           print('Despite timeout of 2 hours, thread %s is still alive'%thread.name)
           
             
except threading.ThreadError as the:
    print('Thread error stack:',the)
    
except Exception as e:
    print('==>{0} for {1} thread has been raised'.format(e, current.name.upper()))
    
finally:
    if(current.isDaemon()):
        print('Daemon reporting =====> Time taken:%d seconds'%(time.time() - start_time))
        print('Daemon reporting =====> PopulateCount',populateCount)
        
print('--->Time taken:%d seconds'%(time.time() - start_time))
