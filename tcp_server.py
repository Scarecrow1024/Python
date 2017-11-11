# coding=utf-8

import socket

s = socket.socket()
s.bind(('localhost', 6969))
s.listen(5)
print('start listen')
while True:
    conn, addr = s.accept()
    while True:
        print(conn, addr)
        print('recv listen')
        data = conn.recv(1024)
        if not data:
            print('lost connect...')
            break
        conn.send(data.upper())

s.close()
