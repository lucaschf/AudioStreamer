import pickle
import socket

import pyaudio

HEADER_SIZE = 10

server_address = socket.gethostname()
server_port = 12000

CHUNK = 2048


def send_data(data, client_socket, header_size=HEADER_SIZE):
    msg = pickle.dumps(data)
    msg = bytes(f"{len(msg):<{header_size}}", 'utf-8') + msg
    client_socket.send(msg)


def receive_data(client_socket, header_size=HEADER_SIZE):
    while True:
        msg_len = 0
        full_msg = b''
        new_msg = True

        while True:
            msg = client_socket.recv(16)

            if new_msg:
                try:
                    msg_len = int(msg[:header_size])
                except Exception:
                    msg_len = 0
                new_msg = False

            full_msg += msg

            if len(full_msg) - header_size == msg_len:
                return pickle.loads(full_msg[header_size:])


def receive_and_play_song(connection):
    p_audio = pyaudio.PyAudio()

    print("Receiving")

    _format = 8
    channels = 2
    rate = 44100
    chunk = 2048

    stream = p_audio.open(format=_format, channels=channels, rate=rate, output=True)

    content = connection.recv(chunk)

    while content:
        stream.write(content)  # plays audio
        content = connection.recv(CHUNK)

    stream.close()
    p_audio.terminate()
    connection.close()
