import socket
s = socket.socket()
host = ''
port = 5000
s.connect((host, port))
print(s.recv(1024).decode())
s.close()