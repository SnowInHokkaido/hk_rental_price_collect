# -*- coding: utf-8 -*-
'''
Target: Collect all the posts published after 2017/04/01 and update the information everyday.
Process
1. Website Access
2. Filter the posts
3. Save the posts into CSV???(Title, content, publish time, url)
4. Everyday updating
'''


import urllib
import urllib2
from bs4 import BeautifulSoup
import time
import datetime
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import re
import sys

def webaccess(urladdress):
    url = urladdress
    req = urllib2.Request(url) #可添加value, header
    res = urllib2.urlopen(req) #可以打开 url 或 request 返回值
    soup = BeautifulSoup(res, "html5lib")
    return soup


def starttime(year,month,day):
    result = datetime.datetime(year,month,day)
    return result
    
begintime = starttime(2017,5,23)

urldict = []
posttime = []

for i in range(1,5):
    url = 'http://bbs.gter.net/forum-1033-'+str(i)+'.html'
    webcontent = webaccess(url)
    trcontent = webcontent.find_all('tr')
    for item in trcontent:
        tdcontent = item.find_all('td', class_ = 'by', limit = 1)
        for item2 in tdcontent:
            date = item2.find_all('span')
            for item3 in date:
                timestr = item3.contents[0]
                t = time.strptime(timestr,'%Y-%m-%d')
                d = datetime.datetime(* t[:6])
                if d > begintime:
                    adrresscontent = item.find_all('th', class_ = 'new')
                    for item4 in adrresscontent:
                        finalresult = item4.find_all('a', class_='xst')
                        for item5 in finalresult:
                            posttime.append(str(d))
                            urldict.append(str(item5['href']))


title = []
content = []

for url in urldict:
    content2 = webaccess(url)
    result2 = content2.find_all(id=re.compile("thread_subject"))
    for tag in result2:
        text1 = tag.get_text()
        title.append(text1)
    
    result3 = content2.find_all('td',class_ = "t_f", limit = 1)
    for floor1 in result3:
        text2 = floor1.get_text()
        content.append(text2)



data = {'url':urldict, 'date':posttime, 'title':title, 'content':content}
urladdress = DataFrame(data, columns = ['url','date','title','content'])
urladdress.to_csv('D:\\Python Script\\WebSpider\\housedata\\house0524.csv',sep=',', encoding = 'utf-8')
