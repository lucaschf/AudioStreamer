import pickle
import socket

from helper import get_audio_from_directory

HEADER_SIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 12000))
s.listen(5)

while True:
    print("awaiting connection....")
    client_socket, address = s.accept()
    print(f"Connection from {address} has been established.")

    library = get_audio_from_directory("../samples")
    msg = pickle.dumps(library)
    msg = bytes(f"{len(msg):<{HEADER_SIZE}}", 'utf-8') + msg
    client_socket.send(msg)
