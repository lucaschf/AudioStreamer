import socket

import pyaudio

server_address = "127.0.0.1"
server_port = 12000
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


client_socket.connect((server_address, server_port))

p_audio = pyaudio.PyAudio()

FORMAT = 8
CHANNELS = 2
RATE = 44100
CHUNK = 2048

stream = p_audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True)

content = client_socket.recv(CHUNK)

while content:
    stream.write(content)  # plays audio
    content = client_socket.recv(CHUNK)

print("Audio played")

stream.close()
p_audio.terminate()
client_socket.close()




