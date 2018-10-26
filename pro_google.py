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

def getAlexaRank(url):
    base_url = 'https://www.alexa.com/siteinfo/'
    comp_url = base_url+url
    html,_ = download(comp_url)
    html = str(html)
    rank = None
    try:
        rank = re.findall('.*global\":([\d].*?)}.*',html)[0]
        print('Rank:',rank)
        return rank
    except Exception:
        return None


def getCountryReg(website):
    addr = 'http://whois.domaintools.com/%s'%website
    _,WS = download(addr)
    lls = []
    for div in WS.find_all('div'):
        if(div.get('id') == 'stats'):
            for ch in div.findChildren('td'):
                lls.append(ch.contents)
    ind = lls.index(['Registrant Country'])
    return lls[ind+1] or None

def getCountry(website):
    addr='http://data.alexa.com/data?cli=10&url=%s'%website
    _,S = download(addr)
    country = None
    for i in S.find_all('country'):
        country = re.findall(r'.*?name=\"(.*?)\".*', str(i))[0]
    return country

def isUsingJS(soup):
    t = soup.find_all('script')
    if len(t) == 0:
        return False
    else:
        return True

def isUsingCSS(html):
    H = str(html)
    if(str(H).find('css') > 0):
        return True
    else:
        return False

def saveHTML(url, content):
    if content is None:
        print('THERE IS NOTHING TO WRITE, RECEIVED NONE')
        return -1
    global path
    fname = None
    try:
        baseName = getBaseName(url)
        fname = path+baseName+'.html'
        ufile = open(fname, 'w')
        ufile.writelines(str(content))
        ufile.close()
    except Exception:
        print('Error occured druing %s saving'%url)


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

def fillNans():
    global siteDetails
    if(siteDetails.get('title',0) == 0):
        siteDetails['title'] = NaN
    if(siteDetails.get('numLinks',0) == 0):
        siteDetails['numLinks'] = NaN
    if(siteDetails.get('descr',0) == 0):
        siteDetails['descr'] = NaN
    if(siteDetails.get('kwords',0) == 0):
        siteDetails['kwords'] = NaN
    if(siteDetails.get('numLinks',0) == 0):
        siteDetails['numLinks'] = NaN
    return 0

def writeDetails(siteDetails):
    try:
        print(siteDetails)
        dataFile.write('URL:-:Title:-:Description:-:Keywords:-:NumLinks')
        sep = ':-:'
        data = '%s%s%s%s%s%s%s%s%s'%(siteDetails['url'],sep, \
                                     siteDetails['title'],sep,\
                                     siteDetails['descr'],sep, \
                                     siteDetails['kwords'],sep, \
                                     siteDetails['numLinks'])
        print('Writing data %s \n'%data)
        data = data[len(sep):]
        dataFile.write(data+'\n')
    except Exception:
        #import sys
        print('FATAL ERROR CANNOT CONTINUE')
        #sys.exit(-1)

def populateSiteDetails(url):
    global siteDetails
    html,contentSoup = download(url)
    if contentSoup is not None:
        saveHTML(url, html)
        siteDetails['url'] = url
        siteDetails['numLinks'] = len(contentSoup.find_all('a'))
        siteDetails['title'] = contentSoup.title.string
        for metaTags in contentSoup.find_all('meta'):
            #print('Populating Tags')
            attrs = metaTags.attrs
            try:
                name = attrs['name']
                dets = attrs['contentSoup']
                if (name == 'title'):
                    siteDetails['title'] = dets
                elif (name == 'description' ):
                    siteDetails['descr'] = dets
                elif(name == 'keywords'):
                    siteDetails['kwords'] = dets
                else:
                    pass
        
            except Exception: pass
    else: pass
    
def prDict(D):
    print('%s\t%s\t%s\t%s\n'%(D['url'],D['title'], D['descr'], D['kwords']))
    return
    #print(D)
    try:
        print('%s\t==>%s\t==>%s\t==>%s\n'%(D['url'],D['title'], D['descr'], D['kwords']))
    except Exception:
        print(D.values())

def clean():
    try:
        scrapeList.close()
        dataFile.close()
    except Exception:
        pass
    return
    
def getBaseName(url):
    print('Incoming ',url)
    import re
    pattern = '[whtps:/]{0,11}.([\w\W\d]{1,})\.*\.ai'
    baseName= re.findall(pattern, url)[0]
    print('URL:%s->%s'%(url,website))
    return baseName
   
path = 'D:/AI/DataSet/'
dataFile=open('D:/AI/dataset.csv', 'a')
dataFile.write('URL:-:Title:-:Description:-:Keywords:-:NumLinks')
siteDetails = {}
#getLinks(1)
clean()

'''
for pageNum in range(0,1):
    print('******************PAGE %d***********************'%pageNum)
    siteNum = pageNum * 10 + 1
    url='https://www.bing.com/search?q=site%3Aai&first='+str(siteNum)
    html,soup = download(url)
    print(soup.title)
    for site in linkExtraction(soup):
        if isDuplicate(site) is False:
            print('Site title is',site)
            populateSiteDetails(site) # Populates and saves HTML file
            fillNans() # Fills NaNs
            writeDetails(siteDetails) # Writes to csv file
            siteDetails = {}
            print('========================================================')
'''