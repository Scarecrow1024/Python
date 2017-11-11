# coding=utf-8

import socket

client = socket.socket()
client.connect(('localhost', 6969))

while True:
    msg = input(">>:").strip()
    if len(msg) == 0:continue
    client.send(msg.encode())
    data = client.recv(1024)
    print('recv:', data.decode('utf-8'))

client.close()
