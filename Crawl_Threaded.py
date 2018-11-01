# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 15:46:59 2018

@author: kkonakan
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 20:41:55 2018

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
    
    def __init__(self, fileName, writer, numLinks):
        super(FetchDetails, self).__init__()
        self.inFile = open('D:/AI/%s.txt'%fileName,'r') # Input links file
        self.DOMAIN = fileName
        self.writer = writer # CSV output writer
        self.crawledList = set()
        self.log = 0 # No log
        self.lock = threading.Lock()
        self.baseName = None
        dataFile='%s/%s.csv'%(path, DOMAIN)
        self.numLinks = numLinks
        
        
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
            #baseName = self.getBaseName(url)
            fname = 'D:/AI/Dataset/%s_%s.html'%(self.baseName, self.DOMAIN)
            print(fname,' is name of the file')
            ufile = open(fname, 'w')
            ufile.writelines(str(content))
            ufile.close()
            size= round(os.path.getsize(fname)/1024)
        except Exception as e:
            print('Error occured during %s saving: %s'%(url,e))
        if self.log == 1:
            print('Returning successfully from saveHTML')
        return size
    
    def download(self,url):
        if self.log == 1:
            print('download requested for ', url)
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
            siteDetails['url'] = url
            siteDetails['numLinks'] = len(contentSoup.find_all('a'))
            siteDetails['title'] = contentSoup.title.string
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
                        siteDetails['title'] = dets
                    elif (name == 'description' ):
                        siteDetails['descr'] = dets
                    elif(name == 'keywords'):
                        siteDetails['kwords'] = dets
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
        pattern = '[whtps:/.]{0,12}([\w\W\d]{1,})\.*\.%s'%self.DOMAIN.lower()
        baseName= re.findall(pattern, url)[0]
        #print('URL:%s->%s'%(url,baseName))
        return baseName
    
    def pr(self, message):
        print(message+'\n')
    
    def transform(self,link):
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
            print('INVALID Link:',link,'\n')
        return base_url
    
    def run(self,skipLines = 0):
        linkFile = self.inFile
        cnt = 1
        global start_time
        while skipLines > 0:
            linkFile.readline()
            skipLines -= 1
        for link in linkFile.readlines():
            link = link.strip()
            #now = time.time()
            print('Current Site# %d / %d: %s'%(cnt,self.numLinks,link ))
            #print('Time elapsed:%d seconds'%(now - start_time))
            cnt += 1
            link = self.transform(link)
            if (link in self.crawledList) or (link is None):
                # Link is a duplicate or an invalid link
                continue
            print('Current link:',link)
            siteDets = self.populateSiteDetails(link)
            print('Length of sitedetails:',len(siteDets))
            self.writer.writerow(siteDets)
            print('Current count:',cnt)
            
        linkFile.close()

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
DOMAIN_list = ['AI','IO']

try:
    start_time = time.time()
    path = 'D:/AI/DataSet/'
    for DOMAIN in DOMAIN_list:
        
        dataFile='%s/%s.csv'%(path, DOMAIN)
        fname = 'D:/AI/%s.txt'%DOMAIN
        # Based on the linecount, start a new thread for every 100 links
        #   Easier to start but harder to write to the dataFile.csv
        
        csvfile=open(dataFile, 'w', encoding='utf-8-sig')
        writer = csv.DictWriter(csvfile, props, restval=NaN)
        writer.writeheader()
        numLinks = getLineCount(fname)
        current = FetchDetails(DOMAIN, writer, numLinks)
        current.name = DOMAIN
        thread_set.append(current)
        print('Starting a thread for %s (%d links)'%(DOMAIN, numLinks))
        current.start()        
        time.sleep(10)
        
    for thread in thread_set:
         print('Waiting for thread %s to join'%thread.name)
         thread.join()
    
except threading.ThreadError as the:
    print('Thread error stack:',the)
except Exception as e:
    print('==>{0} for {1} thread has been raised'.format(e, thread.name.upper()))
finally:
    print('--->Time taken:%d seconds'%(time.time() - start_time))
