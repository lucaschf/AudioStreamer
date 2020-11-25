# coding: utf-8

import socket
import wave

server_port = 12000
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', server_port))
server_socket.listen(0)

CHUNK = 2048  # audio frame size

file_name = '../samples/Nokia-Always here (Ghema 127).wav'
wf = wave.open(file_name, 'rb')

print("server awaiting....")

socket_connection, address = server_socket.accept()

print(type(socket_connection))

print(f"connection established with {address}")

data = wf.readframes(CHUNK)

while data:
    socket_connection.send(data)
    data = wf.readframes(CHUNK)

socket_connection.close()
wf.close()
