import multiprocessing
import socket
import wave

from connection_command import Command
from helpers import get_audio_files_from_directory
from socket_helpers import receive_data, send_data, server_address, server_port


def handle(connection, address):
    import logging

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("process-%r" % (address,))

    try:
        logger.info(f"Connection from {address} has been established.")

        while True:
            data = receive_data(connection)
            if data == "":
                logger.debug(f"No data received. Connection with {address} closed.")
                break

            logger.info(f"Received request {data}")

            if Command.fetch_library in data:
                handle_lib_request(connection)
                break
            if Command.play_song in data:
                handle_play_request(connection, data.get(Command.play_song))
                logger.info("Playing song .......")
                break
            else:
                break
    except RuntimeError:
        logger.exception("Can't handle request")
    finally:
        logger.info("Closing connection.")
        connection.close()


def handle_lib_request(connection):
    library = get_audio_files_from_directory("../samples")
    send_data(library, connection)


def handle_play_request(connection, song):
    wf = wave.open(song.path, 'rb')
    data = wf.readframes(2048)

    print('DATA ' + str(song))

    while data:
        # print('Sending audio')
        connection.send(data)
        data = wf.readframes(2048)

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
        logging.info("Listening")
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
