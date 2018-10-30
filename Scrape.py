# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 20:41:55 2018

@author: kkonakan
"""

import urllib.request as ureq
import bs4
import re
from numpy import NaN

def saveHTML(url, content):
    if content is None:
        print('THERE IS NOTHING TO WRITE, RECEIVED NONE')
        return -1
    print(url, content)
    fname = path
    try:
        site = re.findall('http[s]{0,1}://[w]{0,3}\.([\w\W\d]{1,}).ai.*', url)[0]
        fname = path+site+'.html'
        print(fname)
        ufile = open(fname, 'a')
        ufile.writelines(str(content))
        scrapeList = open('D:/AI/DataSet/ScrapedSites.txt', 'a')
        scrapeList.write(site)
        scrapeList.write('\n')
        ufile.close()
        scrapeList.close()
    except Exception:
        print('Error occured druing %s saving'%url)

path = 'D:/AI/DataSet/'

def isDuplicate(url):
    scrapeList = open('D:/AI/DataSet/ScrapedSites.txt', 'r')
    sites = set(scrapeList.readlines())
    if url in sites:
        return True
    return False

def download(url):
    soup = None
    html = None
    #req = Request(url, headers={'User-agent':'Mozilla/5.0'})
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
                uname = re.findall(rc,url)
                if(len(uname) != 0):
                    link_set.add(uname[0])
            except TypeError:
                print(url,'is causing TypeError')
        else: pass
    return link_set

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

def getLinks(pnum):
    linkList = open('D:/AI/linkList_2.txt', 'a')
    ll = set()
    for pageNum in range(0,pnum+1):
        print('******************PAGE %d***********************'%pageNum)
        siteNum = pageNum * 10 + 1
        url='https://www.bing.com/search?q=site%3Aai&first='+str(siteNum)
        _, soup = download(url)
        print(soup.title)
        for site in linkExtraction(soup):
            if isDuplicate(site) is False:
                    ll.add(site)
                    linkList.write(site)
                    linkList.write('\n')
    linkList.close()

scrapeList = None
dataFile=open('D:/AI/dataset.csv', 'a')
dataFile.write('URL:-:Title:-:Description:-:Keywords:-:NumLinks')
siteDetails = {}
getLinks(2)
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
clean()