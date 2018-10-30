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

def getAlexaRank(url):
    base_url = 'https://www.alexa.com/siteinfo/'
    comp_url = base_url+url
    html,_ = download(comp_url)
    html = str(html)
    rank = None
    try:
        rank = re.findall('.*global\":([\d].*?)}.*',html)[0]
        return rank
    except Exception:
        return None

def getCountryReg(url):
    '''whois limits 5 reqs per day'''
    return None
    addr = 'http://whois.domaintools.com/%s'%url
    _,WS = download(addr)
    lls = []
    for div in WS.find_all('div'):
        if(div.get('id') == 'stats'):
            for ch in div.findChildren('td'):
                lls.append(ch.contents)
    ind = lls.index(['Registrant Country'])
    return lls[ind+1] or None

def getHostCountry(url):
    addr='http://data.alexa.com/data?cli=10&url=%s'%url
    _,S = download(addr)
    country = None
    for i in S.find_all('country'):
        country = re.findall(r'.*?name=\"(.*?)\".*', str(i))[0]
    return country

def isUsingJS(soup):
    t = soup.find_all('script')
    if len(t) == 0:
        return 0
    else:
        return 1

def isUsingCSS(html):
    H = str(html)
    if(str(H).find('css') > 0):
        return 1
    else:
        return 0

def saveHTML(url, content):
    '''
        Saves the file to the disk and returns size of the html file in KB
    '''
    if content is None:
        print('THERE IS NOTHING TO WRITE, RECEIVED NONE')
        return -1
    global path
    fname = None
    size = 0
    try:
        baseName = getBaseName(url)
        fname = path+baseName+'.html'
        ufile = open(fname, 'w')
        ufile.writelines(str(content))
        ufile.close()
        size= round(os.path.getsize(fname)/1024)
    except Exception:
        print('Error occured during %s saving'%url)
    return size

def download(url):
    soup = None
    html = None
    req = ureq.Request(url, headers={'User-agent':'Mozilla/5.0'})
    try:
        html = ureq.urlopen(req, timeout=30).read()
        soup = bs4.BeautifulSoup(html,'lxml')
    except Exception:
        print(url,' site is not allowing bots')
    return html,soup

def fillNans(siteDetails):
    global props
    for prop in props:
        if(siteDetails.get(prop,-12345) == -12345):
            siteDetails[prop] = NaN
        else: pass
    return 0

def populateSiteDetails(url):
    '''
        Retrieves site Details
        Saves the html content to disk for later processing
    '''
    html = None
    contentSoup = None
    siteDetails= {}
    html,contentSoup = download(url)
    if contentSoup is not None and contentSoup.title is not None:
        #print('Content Soup is not NONE:', contentSoup.title)
        siteDetails['url'] = url
        siteDetails['numLinks'] = len(contentSoup.find_all('a'))
        siteDetails['title'] = contentSoup.title.string
        siteDetails['hostedIn'] = getHostCountry(url)
        #siteDetails['RegIn'] = getCountryReg(url)
        siteDetails['AlexaRank'] = getAlexaRank(url)
        siteDetails['CSS'] = isUsingCSS(html)
        siteDetails['JS'] = isUsingJS(contentSoup)
        siteDetails['size'] = saveHTML(url, html)
        for metaTags in contentSoup.find_all('meta'):
            #print('Populating Tags')
            attrs = metaTags.attrs
            if ('name' in attrs.keys() and 'content' in attrs.keys()):
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
        siteDetails['title']= getBaseName(url).upper()
    return siteDetails
    

def getBaseName(url):
    #print('Incoming ',url)
    import re
    pattern = '[whtps:/]{0,11}.([\w\W\d]{1,})\.*\.ai'
    baseName= re.findall(pattern, url)[0]
    #print('URL:%s->%s'%(url,baseName))
    return baseName

def startPopulating():
    linkFile = open('D:/AI/links.txt','r')
    cnt = 1
    global start_time
    for link in linkFile.readlines():
        link = link.strip()
        now = time.time()
        print('Current Site (%d/1017):%s'%(cnt,link))
        print('Time elapsed:%d seconds'%(now - start_time))
        cnt += 1
        siteDets = populateSiteDetails(link)
        #print(siteDets)
        writer.writerow(siteDets)
        #print('Current count:',cnt)
        
    linkFile.close()

start_time = time.time()
path = 'D:/AI/DataSet/'
props = ['url','title','descr','numLinks','kwords','AlexaRank',
         'hostedIn','CSS','JS','size']
csvfile=open(path+'data_11.csv', 'w', encoding='utf-8-sig')
writer = csv.DictWriter(csvfile, props, restval=NaN)
writer.writeheader()
startPopulating()
#soup = populateSiteDetails('http://www.luis.ai')
csvfile.close()
# ERRORS
print('Time taken:%d seconds'%(time.time() - start_time))
try:
    pass
except Exception: 
    pass
finally:
    print('Time taken:%d seconds'%(time.time() - st))
