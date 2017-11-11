import gevent, time, pymysql
import hashlib
import requests
import os
from gevent import monkey

monkey.patch_all()

def get_data():
    db = pymysql.connect("localhost", "root", "", "png")
    cursor = db.cursor()
    try:
        cursor.execute("select id, bianhao, img, is_spider from png where is_spider=0 order by id desc limit 15")
        results = cursor.fetchall()
        data = []
        for row in results:
            data.append(row[2])
        return data
    except:
        return False

def update_data(url,path):
    db = pymysql.connect("localhost", "root", "", "png")
    cursor = db.cursor()
    try:
        sql = "update png set is_spider=1,local_url='%s' where img='%s'" % (str(path), str(url))
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

def down_img(url):
    print(url)
    res = requests.get(url)
    s = hashlib.md5()
    s.update(url.encode('utf-8'))
    md5 = s.hexdigest()
    path = md5[0:2]+'/'+md5[2:4]
    content = res.content
    s = hashlib.md5()
    s.update(url.encode('utf-8'))
    name = s.hexdigest()
    if os.path.exists("C:/Python/_scrapy/miyuansu/miysImg/" + path) is not True:
        os.makedirs("C:/Python/_scrapy/miyuansu/miysImg/" + path)
    img_name = os.path.join("C:/Python/_scrapy/miyuansu/miysImg/"+path, name + '.jpg')
    update_data(url,path+'/'+name+'.jpg')
    with open(img_name, 'wb') as pic:
        pic.write(content)


if __name__ == "__main__":
    while True:
        time.sleep(1)
        data = get_data()
        l = []
        for url in data:
        #     down_img(url)
            l.append(gevent.spawn(down_img, '%s' % url))
        gevent.joinall(l)
