# coding=utf-8
import requests, pymysql, random, time

def login(qq,email,pwd):
    dataForm = {
        'email': email,
        'pwd': pwd
    }

    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0'
    ]
    ua = random.choice(user_agent_list)
    #print(ua)
    headers = {
        'User-Agent': ua,
        'X-Requested-With' : 'XMLHttpRequest',
        'Accept-Language' : 'zh-CN,zh;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'http://www.51yuansu.com',
        'Cache-Control': 'no-cache',
        'Host': 'www.51yuansu.com',
        'Upgrade-Insecure-Requests': '1',
        'Connection': 'keep-alive',
        #'Cookie': '51YSSSID=6jokjq18prn6ed4f5vt5s4ber4;_patm=1510080012;sid=ac15b4fe83c4a8f653700f957dd2e5ea;uid=vqsalaykz%7CJanfer;'
    }
    #res = requests.get('http://www.51yuansu.com/index.php?m=ajax&a=down&id=vcenswyzko', headers=headers)s
    # r = requests.get('http://127.0.0.1:5000/get')
    proxies = {
        "http": '127.0.0.1:38251',
    }
    s = requests.Session()
    res = s.post('http://www.51yuansu.com/?m=login&a=emailLogin', data=dataForm, headers=headers, proxies=proxies)
    cookies = res.cookies.get_dict()
    cookie = ''
    for k in cookies:
        cookie += k+'='+cookies[k]+';'

    db = pymysql.connect("localhost", "root", "", "png")
    cursor = db.cursor()
    try:
        sql = "update account set cookie='%s',status=1 where qq='%s'" % (cookie, qq)
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    print(cookie)

if __name__ == '__main__':
    db = pymysql.connect("localhost", "root", "", "png")
    cursor = db.cursor()
    sql = "select qq,email,password from account where status=0"
    cursor.execute(sql)
    res = cursor.fetchall()
    for item in res:
        login(item[0], item[1], item[2])
