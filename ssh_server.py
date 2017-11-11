# encoding=utf-8
import socket
import os

s = socket.socket()
s.bind(('localhost', 9999))
s.listen(5)

while True:
    conn, address = s.accept()
    print('new connect:', address)
    while True:
        data = conn.recv(1024)
        if not data:
            print('lost conn', address)
            break
        print('exec cmd:', data)
        cmd_res = os.popen(data.decode()).read()
        print('data length:', len(cmd_res))
        conn.send(str(len(cmd_res.encode())).encode('utf-8'))
        ack = conn.recv(1024)
        print(ack)
        conn.send(cmd_res.encode("utf-8"))

s.close()