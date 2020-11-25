import socket

from connection_command import Command
from socket_helpers import send_data, receive_data, server_port, server_address


def play(audio):
    sock = create_connection()

    data = {Command.play_song: audio}
    send_data(data, sock)
    result = receive_data(sock)

    print(result)

    sock.close()


def create_connection():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_address, server_port))
    return sock


def request_library():
    sock = create_connection()
    data = {Command.fetch_library: ''}
    send_data(data, sock)

    result = receive_data(sock)
    sock.close()

    return result


if __name__ == "__main__":
    lib = request_library()
    play(lib[-1])
