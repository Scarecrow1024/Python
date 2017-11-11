# -*- coding: utf-8 -*-
import requests
import json
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import smtplib
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.header import Header

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def sendmail(recv='819681825@qq.com',msg=''):
    # 第三方 SMTP 服务
    mail_host = "smtp.126.com"
    mail_user = "zyf819681825@126.com"
    mail_pass = "zyf941024"
    sender = 'zyf819681825@126.com'

    message = MIMEText(msg, 'html', 'utf-8')
    message['From'] = _format_addr('位置预约好了，点进去看看结果吧 <%s>' % 'zyf819681825@126.com')
    message['Subject'] = Header('一个来自太空深处的提醒...', 'utf-8').encode()
    message['To'] = recv
    message['Cc'] = "819681825@qq.com"

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, [recv, '819681825@qq.com'], message.as_string())
        print("邮件发送成功")
    except Exception as e:
        print(e)
#w = [['946','948','949','951','952'], ['980','983','984','960','961']]
w = [['946','948','948'], ['946','948','948']]
def doSeat(stuid,pswd,seat,date,begin,end,i,j):
    header1 = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'seatlib.hpu.edu.cn:8443',
        'Connection': 'Keep-Alive'
    }
    res1 = requests.get('https://seatlib.hpu.edu.cn:8443/rest/auth?username='+str(stuid)+'&password='+str(pswd)+'',verify=False,headers=header1)
    token = json.loads(res1.content.decode('utf-8'))['data']['token']
    #print(token)

    header3 = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Content-Length': "62",
        'Expect': '100-continue',
        'token': token,
        'Host': 'seatlib.hpu.edu.cn:8443',
        'Connection': 'Keep-Alive'
    }

    post = '"t=1&startTime='+str(begin)+'&endTime='+str(end)+'&seat='+str(seat)+'&date='+date+'&t2=2"'
    print(post)
    res3 = requests.post('https://seatlib.hpu.edu.cn:8443/rest/v2/freeBook',verify=False,headers=header3,data=post)
    json_str = res3.text
    json_obj = json.loads(json_str)
    if json_obj['status']=='success':
        print(json_obj['data'])
        pass
    if json_obj['message'] == '已有1个有效预约，请在使用结束后再次进行选择':
        pass
    if json_obj['message'] == '预约失败，请尽快选择其他时段或座位':
        print(json_obj['message'], seat, i, j)
        seat = w[i][j]
        time.sleep(1)
        j = j+1
        if j != 3:
            doSeat(stuid, pswd, seat, str(date), begin, end, i, j)
    if json_obj['message'] == '系统可预约时间为 19:30 ~ 23:30':
        time.sleep(1)
        print(json_obj['message'], seat, i, j)
        doSeat(stuid, pswd, seat, str(date), begin, end,i,j)
    return json_str


data = [['3 7','421520', '945', '450', '690', 0, 0], ['31140 23456', '945', '840', '1080', 1, 0]]
tim = time.time()
local = time.localtime(tim + 3600 * 24)
date = time.strftime("%Y-%m-%d", local)
sendall = ''
for item in data:
    json_str = doSeat(item[0],item[1],item[2],str(date),item[3],item[4],item[5],item[6])
    json_obj = json.loads(json_str)
    sendstr = 'student:'+str(item[0])+'<br>'
    if json_obj['status'] == 'success':
        for item in json_obj['data']:
            tmp =  item+':'+str(json_obj['data'][str(item)])+"<br>"
            sendstr = sendstr + tmp
            sendall = sendall + sendstr + "<br>"
        sendmail('646780854@qq.com', sendall)
    else:
        if json_obj['message']=='系统可预约时间为 19:30 ~ 23:30':
            tmp = json_obj['message']
            sendstr = sendstr + tmp
            sendall = sendall + sendstr + "\n"
        elif json_obj['message']=='已有1个有效预约，请在使用结束后再次进行选择':
            sendstr = sendstr + json_obj['message']
            sendall = sendall + sendstr + "\n"
        else:
            print(json_obj['message'])
#sendmail('819681825@qq.com', sendall)
