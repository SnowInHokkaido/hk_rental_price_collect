# -*- coding: utf-8 -*-
'''
PS： BS4所有的返回值都是对象
Beautiful Soup将复杂HTML文档转换成一个复杂的树形结构,
每个节点都是Python对象,
所有对象可以归纳为4种: Tag , NavigableString , BeautifulSoup , Comment .

搜索逻辑：
深度优先策略 VS 广度优先策略

去重策略：
1. 使用MD5算法，将URL映射为128位数字，每次进行对比。缺点：耗时大
2. 使用布隆过滤器

'''

import urllib2
from bs4 import BeautifulSoup
import lxml 
import re

import time
import datetime

import pandas as pd
import numpy as np
import sys

def webaccess(urladdress, timeout = 30):
    url = urladdress
    req = urllib2.Request(url) #可添加value, header， 以及连接时间
    try:
        res = urllib2.urlopen(req, timeout = timeout) #利用try...except来避免连接失败使程序停止
        soup = BeautifulSoup(res, 'html5lib')# 利用BS4解析返回的网页代码, 可更换解析库： html5lib, lxml, xml。 html5lib会按照浏览器的方式解析
        return soup
    except:
        return False 


def starttime(year, month, day):
    result = datetime.datetime(year, month, day)
    return result



def JituoURLSearch(year = 2017, month = 4, day = 1 , searchrange = 10, timeout = 30):
    begintime = starttime(year, month, day).date()
    urldict = []
    post_time = []
    for i in range(1,searchrange):
        url = 'http://bbs.gter.net/forum-1033-'+str(i)+'.html'
        webcontent = webaccess(url, timeout = timeout)
        if webcontent == False:
            pass
        else:
            tbodycontent = webcontent.find_all('tbody', id=re.compile("normalthread_"))
            for item in tbodycontent:
                for item2 in item.find_all('td', class_ = 'by', limit = 1):
                    posttime = item2.em.span.get_text()
                    posttime = time.strptime(posttime,'%Y-%m-%d')
                    posttime = datetime.datetime(* posttime[:6])
                    if posttime.date() > begintime:
                        urldict.append(item.tr.td.a['href'])
                        post_time.append(posttime.date())
    
    data = {'time':post_time, 'url': urldict}
    urladdress =  pd.DataFrame(data, columns = ['time','url'])
    urladdress = urladdress.drop_duplicates(subset = 'url') # drop duplicated url
    return urladdress


def JituoContent(urldict):
    urllist = list(urldict)
    title = []
    finalcontent = []
    for url in urllist:
        content = webaccess(url, timeout = 30)

        if content == False:
            title.append('False')
            finalcontent.append('False')
        else:
            result = content.find_all(id=re.compile("thread_subject"))
            for tag in result:
                title.append(tag.contents[0])       

            result1 = content.find_all('td',class_ = "t_f", limit = 1)
            for description in result1:
                text = description.get_text()
                finalcontent.append(text)
    
    data = {'title' : title, 'content' : finalcontent}
    final = pd.DataFrame(data, columns = ['title','content'])
    return final
 
    
def GangpiaoURLSearch(year = 2017, month = 4, day = 1 , searchrange = 10, timeout = 30):
    begintime = starttime(year, month, day).date()
    urldict = []
    post_time = []
    for i in range(1,searchrange):
        url = 'http://www.gangpiaoquan.com/thread-2-' + str(i) +'.html&orderby=postdate'
        webcontent = webaccess(url, timeout = timeout)
        if webcontent == False:
            pass
        else:
            tbodycontent = webcontent.find_all('div', class_= 'box-right-content')
            ttime = webcontent.find_all('span', class_= 'mr10')
            for item in tbodycontent:
                urldict.append(item.a['href'])
            for item2 in ttime:
                post_time.append(item2.get_text())

    data = {'time':post_time, 'url': urldict}
    result =  pd.DataFrame(data, columns = ['time','url'])
    result = result.drop_duplicates(subset = 'url')
    result['time'] = pd.to_datetime(result['time'], format = '%Y-%m-%d', errors = 'ignore')
    result = result[result.time > pd.to_datetime(begintime, format = '%Y-%m-%d')]
    result = result.reset_index(drop = True)
    return result

def GangpiaoContent(urldict):
    urllist = list(urldict)
    title = []
    finalcontent = []
    for url in urllist:
        webcontent = webaccess(url, timeout = 30)
        if webcontent == False:
            title.append('False')
            finalcontent.append('False')
        else:
            ttitle = webcontent.find_all('div', class_= 'read-page-title', limit = 1)
            tbodycontent = webcontent.find_all('div', class_= 'editor_content', limit = 1)
            for item1 in tbodycontent:
                finalcontent.append(item1.get_text())
            for item2 in ttitle:
                title.append(item2.get_text())
    
    data = {'title' : title, 'content' : finalcontent}
    final = pd.DataFrame(data, columns = ['title','content'])
    return final


# Main函数
if __name__ == "__main__":
    url_1 = JituoURLSearch(year = 2017, month = 7, day = 1 , searchrange = 2, timeout = 30)
    urldict_1 = url_1['url'].values
    info_1 = JituoContent(urldict_1)
    Jituo = pd.concat((url_1, info_1), axis = 1)
    
    url_2 = GangpiaoURLSearch(year = 2017, month = 7, day = 1 , searchrange = 2, timeout = 30)
    urldict_2 = url_2['url'].values
    info_2 = GangpiaoContent(urldict_2)
    Gangpiaoquan = pd.concat((url, info), axis = 1)
    Houseinfo = Jituo.append(Gangpiaoquan, ignore_index = True)
    Houseinfo.to_csv('D:\\Python Script\\WebCrawler\\Housedata\\testing.csv',sep=',', encoding = 'utf-8')
    print Houseinfo
