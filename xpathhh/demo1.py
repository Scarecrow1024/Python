from lxml import etree
from urllib import request

r = request.urlopen('https://douban.com')
res = r.read().decode()
html = etree.HTML(res)
result = html.xpath('//*[@id="anony-movie"]/div[1]/div[2]/div[2]/div/ol//li/a')
print(result[2].text, '--->', result[2].get('href'))
