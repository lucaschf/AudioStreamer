import socket

from helpers import get_audio_files_from_directory
from socket_helpers import send_data, server_port, receive_data

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), server_port))
s.listen(5)

while True:
    print("awaiting connection....")
    client_socket, address = s.accept()
    print(f"Connection from {address} has been established.")

    # data = receive_data(client_socket)

    library = get_audio_files_from_directory("../samples")
    send_data(library, client_socket)
