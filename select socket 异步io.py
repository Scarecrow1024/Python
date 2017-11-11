import select, socket

server = socket.socket()

inputs = [server, ]
outputs = []
server.bind(('localhost', 9699))
server.listen(1000)

server.setblocking(False) #no block

while True:
    readable, writeable, exceptional = select.select(inputs, outputs, inputs)
    for r in readable:
        if r is server:
            conn, addr = server.accept()
            print('new connect:', addr)
            inputs.append(conn)
        else:
            data = r.recv(1024)
            print('recv data:',data)
            r.send(data)
            print('send done')

    for e in exceptional:
        if e in outputs:
            outputs.remove(e)
        inputs.remove(e)