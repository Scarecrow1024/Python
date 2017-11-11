import gevent, time, pymysql
from PIL import Image
from gevent import monkey

monkey.patch_all()

def get_data():
    db = pymysql.connect("localhost", "root", "", "png")
    cursor = db.cursor()
    try:
        cursor.execute("select id, bianhao, local_url, width, height from png where width=0 limit 20")
        results = cursor.fetchall()
        data = []
        for v in results:
            data.append([v[0],v[2]])
        return data
    except:
        return False

def update_data(pid,width,height):
    db = pymysql.connect("localhost", "root", "", "png")
    cursor = db.cursor()
    try:
        sql = "update png set width='%s',height='%s' where id='%s'" % (width, height, pid)
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

def down_img(pid, local_url):
    Im = Image.open("C:/Python/_scrapy/miyuansu/img1/"+local_url)
    size = Im.size
    print(size[0], size[1])
    update_data(pid,size[0],size[1])


if __name__ == "__main__":
    while True:
        time.sleep(1)
        data = get_data()
        l = []
        for item in data:
            l.append(gevent.spawn(down_img,item[0],item[1]))
        gevent.joinall(l)
