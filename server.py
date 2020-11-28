import logging
import multiprocessing
import socket
import threading
import wave

from action import Action
from helpers import get_song_library
from socket_helpers import receive_data, send_data, server_address, server_port, CHUNK

logging.basicConfig(level=logging.DEBUG)


def handle(connection, address):
    logger = logging.getLogger("process-%r" % (address,))

    try:
        logger.info(f"Connection from {address} has been established.")

        while True:
            data = receive_data(connection)
            if data == "":
                logger.debug(f"No data received. Connection with {address} closed.")
                break

            logger.info(f"Received request  {str(data)}")

            if Action.fetch_library in data:
                handle_lib_request(connection)
                logger.info("Closing connection.")
                connection.close()
                break
            if Action.play_song in data:
                th = threading.Thread(target=handle_play_request, args=[connection, data.get(Action.play_song)])
                th.start()
                break
            else:
                break
    except RuntimeError:
        logger.exception("Can't handle request")
        connection.close()


def handle_lib_request(connection):
    library = get_song_library("../music")
    send_data(library, connection)


def handle_play_request(connection, song):
    wf = wave.open(song.path, 'rb')
    data = wf.readframes(CHUNK)

    while data:
        try:
            connection.send(data)
            data = wf.readframes(2048)
        except ConnectionResetError:
            print('Connection closed by client')
            break

    connection.close()
    wf.close()


class Server(object):
    def __init__(self, hostname, port):
        import logging

        self.logger = logging.getLogger("")
        self.hostname = hostname
        self.port = port
        self.socket = None

    def start(self):
        self.logger.info("Awaiting connection...")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.hostname, self.port))
        self.socket.listen(1)

        while True:
            conn, address = self.socket.accept()
            self.logger.info("Connection accepted...")
            _process = multiprocessing.Process(target=handle, args=(conn, address))
            _process.daemon = True
            _process.start()
            self.logger.debug("Started process %r", _process)


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    server = Server(server_address, server_port)

    try:
        server.start()
    except RuntimeError:
        logging.exception("Unexpected exception")
    finally:
        logging.info("Shutting down")
        for process in multiprocessing.active_children():
            logging.info("Shutting down process %r", process)
            process.terminate()
            process.join()

    logging.info("All done")
