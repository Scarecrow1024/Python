# -*- coding: utf-8 -*-
import requests, pymysql
import redis, time
import hashlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import xlrd
import os
import gevent
from gevent import monkey

monkey.patch_all()

class Miys(object):
    def __init__(self):
        # self.browser = webdriver.PhantomJS(service_args=['--load-images=true', '--disk-cache=true'])
        # self.browser.set_window_size(1366, 768)
        # self.wait = WebDriverWait(self.browser, 2)
        
        self.detail_num = 0
        self.__connRedis = redis.Redis(host='@@@@@@@@@@', port=6379, db=1, password='******')
        self.__connMysql = pymysql.connect("127.0.0.1", "root", "", "png", charset='utf8')
        
        self.headers = {
            'content-type': 'application/json',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

    def getKeyWord(self):
        cursor = self.__connMysql.cursor()
        cursor.execute("select id, kw from keyword where stat=0 limit 1")
        results = cursor.fetchone()

        try:
            sql = "update keyword set stat=1 where id='%s'" % (results[0])
            cursor.execute(sql)
            self.__connMysql.commit()
        except:
            self.__connMysql.rollback()
            
        cursor.close()
        keyword = results[1]
        res = requests.get('http://www.51yuansu.com/index.php?m=Index&a=pinYin&k=%s' % keyword, headers=self.headers, stream=True)
        return res.json()

    def doSearch(self):
        json = self.getKeyWord()
        # self.browser.get('http://www.51yuansu.com/search/%s.html' % json['py'])
        # isLoad = self.wait.until(
        #     EC.title_contains('元素')
        # )
        # if isLoad:
        #     js = "var q=document.documentElement.scrollTop=10000"
        #     self.browser.execute_script(js)
        #     time.sleep(1)
        #     self.wait.until(
        #         EC.presence_of_element_located((By.XPATH, "//*[@id='f-content']"))
        #     )
        #     #return page
        #     return self.browser.page_source
        #json['py'] = 'siliuji'
        res = requests.get('http://www.51yuansu.com/search/%s.html' % json['py'])
        data = {}
        data['py'] = json['py']
        data['content'] = res.content
        return data

    #获取页码链接
    def getPages(self):
        data = self.doSearch()
        html = data['content']
        py = data['py']
        link = 'http://www.51yuansu.com/index.php?m=Index&a=fenlei&k={kw}&p={page}'
        doc = pq(html)
        #如果存在页数就获取最大页码
        #不存在就获取当前页链接
        if doc.find('.pager-wrap'):
            pages = []
            max_page = doc.find('.pager-content > a:last').text()
            self.detail_num = int(max_page)*30
            for page in range(1, int(max_page)+1):
                pages.append(link.format(kw=py, page=page))
            return pages
        else:
            #直接解析页面存到set
            self.getDetailLink('http://www.51yuansu.com/search/{kw}.html'.format(kw=py))

    def parsePage(self):
        pages = self.getPages()
        l = []
        for page in pages:
            time.sleep(0.1)
            l.append(gevent.spawn(self.getDetailLink, page))
        gevent.joinall(l)


        # for page in pages:
        #     res = requests.get(page)
        #     print(res.text)

    def getDetailLink(self, page):
        r = requests.get(page)
        html = r.content
        doc = pq(html)
        items = doc.find('.f-content > .i-flow-item > p > a').items()
        data = []
        for item in items:
            url = item.attr('href')
            data.append((str(url),))
            self.redisSet(url)
            print(url)
        db = pymysql.connect("localhost", "root", "", "png")
        try:
            with db.cursor() as cursor:
                sql = "insert into png2 (detail_url) values (%s)"
                cursor.executemany(sql,data)
            db.commit()
        except:
            print('已存在')
        finally:
            db.close()

    def redisSet(self, url):
        redis = self.__connRedis
        m = hashlib.md5()
        m.update(url.encode('UTF-8'))
        url = m.hexdigest()
        if redis.sadd('set', url):
            pass
            # 插入队列
            #redis.lpush('list', url)
            # db = pymysql.connect("localhost", "root", "", "png")
            # try:
            #     with db.cursor() as cursor:
            #         sql = "insert into png2 (detail_url) values ('%s')" % str(url)
            #         cursor.execute(sql)
            #     db.commit()
            # finally:
            #     db.close();
        else:
            pass

    def insert2DB(self):
        xlrd.Book.encoding = "utf-8"
        data = xlrd.open_workbook('keyword.xls')
        table = data.sheets()[0]
        keywords = table.col_values(0)
        status = table.col_values(1)
        db = pymysql.connect("localhost", "root", "", "png")
        cursor = db.cursor()
        for k,keyword in enumerate(keywords):
            try:
                sql = "insert into keyword (kw,hot)values('%s','%s')" % (str(keyword), str(status[k]))
                print(sql)
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()

    def main(self):
        while True:
            self.parsePage()
if __name__ == '__main__':
    miys = Miys()
    #print(miys.redisSet())
    #exit()
    miys.main()
