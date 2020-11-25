import socket

from connection_command import Command
from socket_helpers import server_address, server_port, send_data

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_address, server_port))


def request_lib():
    send_data({Command.fetch_library: ''}, client_socket)
