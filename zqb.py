#coding=utf-8
import requests
from pyquery import PyQuery as pq
import time
import csv
import os
import gevent
from gevent import monkey

monkey.patch_all()

#获取版面列表
def getPageList(url):
    print('开始获取版面链接...')
    base_url = 'http://zqb.cyol.com/html/2017-08/25/'
    res = requests.get(url)
    html = res.text
    doc = pq(html)
    pagelist = doc.find("div[id='pageList'] a").items()
    lst = []
    for item in pagelist:
        lst.append(base_url+item.attr('href'))
    print('获取版面链接完成')
    return lst

#根据版面列表获取文章链接
def getTitleList(url):
    base_url = 'http://zqb.cyol.com/html/2017-08/25/'
    hrefs = getPageList(url)
    lst = []
    for href in hrefs:
        res = requests.get(href)
        time.sleep(1)
        html = res.text
        doc = pq(html)
        titleList = doc.find("div[id='titleList'] a").items()
        for item in titleList:
            lst.append(base_url+item.attr('href'))
    return lst

#根据版面列表获取文章链接
def getTitleList1(url):
    base_url = 'http://zqb.cyol.com/html/2017-08/25/'
    lst = []
    res = requests.get(url)
    time.sleep(1)
    html = res.text
    doc = pq(html)
    titleList = doc.find("div[id='titleList'] a").items()
    for item in titleList:
        lst.append(base_url+item.attr('href'))
    for i in lst:
        data = parsePage(i)
        write2csv(data)
        print(data)

#解析页面
def parsePage(url):
    res = requests.get(url)
    html = res.content
    doc = pq(html)
    title = doc.find("div[class='text_c'] h1").text()
    ps = doc.find("div[id='ozoom'] p").items()
    content = ''
    for p in ps:
        content += p.text()
    return (title,content.replace(u'\xa0', u''))

#写入csv文件
def write2csv(dic):
    with open("C:\\Python\\zqb.csv", "a+", newline='') as data:
        csver = csv.writer(data, dialect=("excel"))
        if os.path.exists("C:\\Python\\zqb.csv") == False:
            csver.writerow([
                    "title",
                    "content"
                ])
        csver.writerows([dic])

#运行主函数
def main(start_url):
    pageList = getPageList(start_url)
    print(pageList)
    print('正在获取文章链接')
    l = []
    for url in pageList:
        l.append(gevent.spawn(getTitleList1, '%s' % url))
    gevent.joinall(l)
    exit()
    pass

if __name__ == "__main__":
    main('http://zqb.cyol.com/html/2017-08/25/nbs.D110000zgqnb_01.htm')
