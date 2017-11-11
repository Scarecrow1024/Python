import gevent, time
from urllib import request
from gevent import monkey

monkey.patch_all()

def f(url):
    try:
        q = request.urlopen(url)
        data = q.read()
        print('%d bits recv from %s' % (len(data), url))
    except TracebackType as e:
        print(e)

urls = ['https://www.python.org/', 'https://yahoo.com', 'https://github.com']

start1 = time.time()
for i in urls:
    f(i)
print("chuanxing:", time.time()-start1)
start2 = time.time()
l = []
for url in urls:
    l.append(gevent.spawn(f, '%s' % url))

gevent.joinall(l)
print(l)
print("xiecheng:", time.time()-start2)