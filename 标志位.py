# coding=utf-8
import threading, time
"""
    简单信号量栗子，模拟黄绿灯
"""
event = threading.Event()

def lighter():
    count = 0
    event.set() #设置信号量为绿灯，车可以通过
    while True:
        if count > 10 and count < 20:
            event.clear() #清空信号量为红灯车不能通过
            print("\033[41;1mred light is on...\033[0m")
        elif count > 20:
            event.set() #重新设置信号量
            count = 0
        else:
            print("\033[42;1mgreen light is on...\033[0m")
        time.sleep(1)
        count += 1

def car(name):
    while True:
        if event.is_set(): #检查是否存在信号量
            print("%s running..." % name)
            time.sleep(1)
        else:
            print("[%s] red light, warting..." % name)
            event.wait() #等待信号量再继续向下运行
            print("\033[42;1mgreen light is on... going...\033[0m")

if __name__ == "__main__":
    l = threading.Thread(target=lighter,)
    l.start()
    c = threading.Thread(target=car, args=("Tesla",))
    c.start()
