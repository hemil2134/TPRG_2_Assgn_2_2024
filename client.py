'''
TPRG 2131 Fall 2024 Assignment 2.
Dec, 2024
Hemil Prajapati (100942152).
This program is strictly my own work. Any material
beyond course learning materials that is taken from
the Web or other sources is properly cited, giving.
credit to the original author(s).
'''

# Import the socket module to enable communication between devices
import socket

# Create a socket object for the client
s = socket.socket()

# Define the server's IP address and port number
host = ''
port = 5000

# Connect to the server using the host and port
s.connect((host, port))

# Receive data sent by the server and decode it to a string
print(s.recv(1024).decode())

# Close the connection to the server
s.close()
