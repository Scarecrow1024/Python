import gevent

def foo1():
    print('foo1 ing....')
    gevent.sleep(1)
    print('foo1 again...')

def foo2():
    print('foo2 ing....')
    gevent.sleep(2)
    print('foo2 done...')

def foo3():
    print('foo3 ing...')
    gevent.sleep(3)
    print('foo3 done')

if __name__ == "__main__":
    gevent.joinall(
        [
            gevent.spawn(foo1),
            gevent.spawn(foo2),
            gevent.spawn(foo3)
        ]
    )