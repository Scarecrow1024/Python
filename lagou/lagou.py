# -*- coding:utf-8 -*-
__author__ = 'ZYF'
__data__ = '2017.04.19'

import requests
import json
import time
import xlwt
import random
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import gevent
from gevent import monkey

monkey.patch_all()

"""
不显示SSL警报
"""
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Spider(object):
    #def __init__(self):
    #    self.keyword = input('请输入职位：').strip()

    """
    获取数据
    """
    def getData(self, url):
        user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0',
                       'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ \(KHTML, like Gecko) Element Browser 5.0',
                       'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
                       'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
                       'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) \Version/6.0 Mobile/10A5355d Safari/8536.25',
                       'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \Chrome/28.0.1468.0 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36 OPR/37.0.2178.32',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
                       'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.9.2.1000 Chrome/39.0.2146.0 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36 Core/1.47.277.400 QQBrowser/9.4.7658.400',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.154 Safari/537.36 LBBROWSER',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36 TheWorld 7',
                       'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)']
        index = random.randint(0, 20)
        user_agent = user_agents[index]
        # url = 'https://www.lagou.com/jobs/positionAjax.json?first=true&pn=%d&kd=%s&city=杭州' % (pages, self.keyword)
        headers = {
                'User_agent': user_agent,
                'cookie': 'JSESSIONID=B42E9196AE2F5EA2275D733C7897B616; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1493351326; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1493351347; _ga=GA1.2.1615193203.1493351326; _gat=1; user_trace_token=20170428114844-93bd8545-2bc5-11e7-b417-5254005c3644; LGSID=20170428114844-93bd89d6-2bc5-11e7-b417-5254005c3644; PRE_UTM=m_cf_cpt_baidu_pc; PRE_HOST=bzclk.baidu.com; PRE_SITE=http%3A%2F%2Fbzclk.baidu.com%2Fadrc.php%3Ft%3D06KL00c00fATEwT0o_4m0FNkUsaR8sFu000002iV8H300000xiYubb.THL0oUhY0A3qrHcdrjn1PWKxpA7EgLKM0Znqm19-njNBn1Rsnj0smyfzu0Kd5H6LwjD4nHb4PDfkwDFAfYmswD7jwRfdPHc3f17DP17D0ADqI1YhUyPGujYzrHfYP1R3PjczFMKzUvwGujYkP6K-5y9YIZK1rBtEILILQhk9uvqdQhPEUitOIgwVgLPEIgFWuHdVgvPhgvPsI7qBmy-bINqsmsKWThnqnW6zn1T%26tpl%3Dtpl_10085_14394_1%26l%3D1052356004%26attach%3Dlocation%253D%2526linkName%253D%2525E6%2525A0%252587%2525E9%2525A2%252598%2526linkText%253D%2525E3%252580%252590%2525E6%25258B%252589%2525E5%25258B%2525BE%2525E7%2525BD%252591%2525E3%252580%252591%2525E5%2525AE%252598%2525E7%2525BD%252591-%2525E4%2525B8%252593%2525E6%2525B3%2525A8%2525E4%2525BA%252592%2525E8%252581%252594%2525E7%2525BD%252591%2525E8%252581%25258C%2525E4%2525B8%25259A%2525E6%25259C%2525BA%2526xp%253Did%28%252522m4e160542%252522%29%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FH2%25255B1%25255D%25252FA%25255B1%25255D%2526linkType%253D%2526checksum%253D250%26ie%3Dutf-8%26f%3D3%26tn%3D92583360_hao_pg%26wd%3Dlagou%26oq%3Dlagou%26rqlang%3Dcn%26ssl_sample%3Dnormal%26rsp%3D1; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F%3Futm_source%3Dm_cf_cpt_baidu_pc; LGRID=20170428114905-a0274d5e-2bc5-11e7-b417-5254005c3644; LGUID=20170428114844-93bd8bcb-2bc5-11e7-b417-5254005c3644; _putrc=9F25F1AC70195174; login=true; unick=%E5%B1%B1%E5%A4%96%E5%B0%8F%E6%A5%BC%E5%A4%9C%E5%90%AC%E9%9B%A8; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=15; index_location_city=%E5%85%A8%E5%9B%BD'
            }
        proxies = {"http": "http://127.0.0.1:8087"}
        data = requests.get(url, verify=False, headers=headers, proxies=proxies)
        return data.text

    # 返回一个小列表存一页的数据
    def getPosition(self, url):
        res = self.getData(url)
        try:
            data = json.loads(res)
            result = data['content']['positionResult']['result']
            l_list = []
            if result is not None:
                for i in result:
                    main = []
                    main.append(i['companyFullName'])
                    main.append(i['financeStage'])
                    main.append(i['positionName'])
                    main.append(i['positionLables'])
                    main.append(i['salary'])
                    main.append(i['city'])
                    main.append(i['education'])
                    main.append(i['workYear'])
                    main.append(i['jobNature'])
                    main.append(i['createTime'])
                    l_list.append(main)
            else:
                l_list.append([])
            return l_list
        except json.decoder.JSONDecodeError as e:
            print(e)
    def saveAll(self, page, keyword):
        book = xlwt.Workbook()
        sheet = book.add_sheet(str(keyword), cell_overwrite_ok=True)
        container = self.getAll(page, keyword)
        print('准备将数据存入表格...')
        heads = [u'公司全名', u'融资状况', u'工作名称', u'标签', u'薪酬', u'城市', u'学历要求', u'经验要求', u'工作类型', u'数据创建时间']
        ii = 0
        for head in heads:
            sheet.write(0, ii, head)
            ii += 1
        i = 1
        for list in container:
            j = 0
            for one in list:
                sheet.write(i, j, str(one))
                j += 1
            i += 1
        book.save(str(keyword) + '-2.xls')
        print('录入成功！')

    # 获取全部页数
    def getAll(self, page, keyword):
        #pn = input('输入要爬取得页数：')
        pn = page
        container = []
        for page in range(1, int(pn)+1):
            self.url = 'http://www.lagou.com/jobs/positionAjax.json?px=new&first=true&pn=' + str(page) + '&kd=' + str(
                    keyword)
            po_list = self.getPosition(self.url)
            time.sleep(0)
            print('第', page, u'页完毕')
            #print(po_list)
            try:
                container = container + po_list
            except TypeError as e:
                print(e)
                container = container
        return container


if __name__ == "__main__":
    spider = Spider()

    l = []
    data = [('286', 'php')]
    for dt in data:
        l.append(gevent.spawn(spider.saveAll, dt[0], dt[1]))
    gevent.joinall(l)

