import socket


#建立连接


while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('192.168.6.231', 100))
    s.send(b'sabi')
    data=s.recv(1024)

    print(data)
