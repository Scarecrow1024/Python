import requests
from PIL import Image
import sys
import time
import pyocr.builders
from pyquery import PyQuery as pq
import smtplib
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.header import Header

class SendM(object):
    def __init__(self, **kwargs):
        self.reciver = kwargs['reciver']
        self.msgs = kwargs['msg']

    def _format_addr(self,s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def send_mail(self):
        from_addr = 'zyf819681825@126.com'
        password = 'zyf941024'
        to_addr = self.reciver
        smtp_server = 'smtp.126.com'
        msgs = self.msgs
        msg = MIMEText(msgs, 'html', 'utf-8')
        msg['From'] = self._format_addr('玩命抢座了，点进去看结果 <%s>' % from_addr)
        msg['To'] = self._format_addr('<%s>' % to_addr)
        msg['Subject'] = Header('一封来自太空深处的邮件...', 'utf-8').encode()
        server = smtplib.SMTP(smtp_server, 25)
        #server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()

class DoSelf(object):
    def __init__(self,stuid,pawd,seat,start,end):
        self.re = requests.Session()
        self.stu = stuid
        self.paw = pawd
        tim = time.time()
        local = time.localtime(tim)
        date = time.strftime("%Y-%m-%d", local)
        self.date = date
        self.seat = seat
        self.start = start
        self.end = end
        """
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Length': '51',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'http://seatlib.hpu.edu.cn',
            'Connection': 'keep-alive'
        }
        """

    def imgToString(self):
        tools = pyocr.get_available_tools()
        if len(tools) == 0:
            print("No OCR tool found")
            sys.exit(1)
        tool = tools[0]
        img = Image.open("captcha.png")
        size = img.size
        for i in range(0, size[0]):
            for j in range(0, size[1]):
                r, g, b = img.getpixel((i, j))
                if r == 138 or r == 223 or r == 224:
                    r = 255
                    g = 255
                    b = 255
                img.putpixel((i, j), (r, g, b))
                img.save("img1.png", "png")
        return tool.image_to_string(img)

    def doLogin(self):
        captcha_text = self.re.get('http://seatlib.hpu.edu.cn/simpleCaptcha/captcha')
        f = open('captcha.png','wb')
        f.write(captcha_text.content)
        f.close()
        capt = self.imgToString()
        print(capt)
        formData = {
            'username': self.stu,
            'password': self.paw,
            'captcha': capt
        }
        res = self.re.post('http://seatlib.hpu.edu.cn/auth/signIn', data=formData)
        if (res.url != 'http://seatlib.hpu.edu.cn/login'):
            return True
        else:
            self.doLogin()

    def seatilib(self):
        self.doLogin()
        self.re.get('http://seatlib.hpu.edu.cn/simpleCaptcha/captcha')
        formData = {
            'date': self.date,
            'seat': self.seat,
            "start": self.start,
            "end": self.end
        }
        res = self.re.post('http://seatlib.hpu.edu.cn/selfRes', data=formData)
        return res

if __name__ == "__main__":
    """
    上午七点半：450
    上午十一点半：690
    下午两点：840
    下午六点：1080
    174:1416
        311309010130
        243616
        311312020212
        214421
    46: 981
        311408000407
        421520
        311408000403
        123456
    47: 945
        311408000402
        230642
        311408000701
        987654
    48: 980
        311501030134
        000000
        311415020102
        000000
    """
    data = [['311309010130','243616','1416','450','690'], ['311312020212','214421','1416','840','1080']]

    data = [['311408000407','421520','981','450','690'], ['311408000403','123456','981','840','1080']]

    data = [['311408000402','230642','945','450','690'], ['311408000701','987654','945','840','1080']]

    data = [['311501030134','000000','980','450','690'], ['311415020102','000000','980','840','1080']]
    #data = [['311614010120', '110206', '1203', '1020', '1080'],['311614010120', '110206', '1203', '1020', '1080']]
    for item in data:
        doit = DoSelf(item[0],item[1],item[2],item[3],item[4])
        res = doit.seatilib()
        print(res.url)
        doc = pq(res.text)
        msg = doc("div[class='layoutSeat'] dd").text()
        print(msg)
        kwargs = {'reciver': '819681825@qq.com', 'msg': msg}
        s = SendM(**kwargs)
        s.send_mail()
        time.sleep(1)
        msg = doc("div[class='layoutSeat'] dd").text()
        kwargs = {'reciver': 'zyf819681825@126.com', 'msg': msg}
        s = SendM(**kwargs)
        s.send_mail()
