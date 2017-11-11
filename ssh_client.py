# encoding=utf-8
import socket

c = socket.socket()
c.connect(('localhost', 9999))

while True:
    msg = input('>>:').strip()
    if len(msg) == 0:
        continue
    c.send(msg.encode('utf-8'))
    cmd_res_size = c.recv(1024)
    c.send(b'ready to recv')
    recvd_size = 0
    while recvd_size != int(cmd_res_size.decode()):
        cmd_res = c.recv(1024)
        recvd_size += len(cmd_res)
        print(cmd_res.decode())
    else:
        print('cmd res receive done')
c.close()