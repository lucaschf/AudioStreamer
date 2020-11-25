import socket

from flask import Flask, render_template, request

from audio_file import AudioFile
from connection_command import Command
from socket_helpers import receive_data, send_data, server_port, server_address, receive_and_play_song

app = Flask(__name__)


def create_connection():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_address, server_port))
    return sock


def request_play(song):
    connection = create_connection()

    data = {Command.play_song: song}
    send_data(data, connection)

    receive_and_play_song(connection)

    connection.close()


def request_library():
    sock = create_connection()
    data = {Command.fetch_library: ''}
    send_data(data, sock)

    result = receive_data(sock)
    sock.close()

    return result


@app.route('/')
def index():
    library = request_library()
    return render_template('library.html', title="library", library=library)


@app.route('/play_song', methods=['POST', ])
def play_song():
    name = request.form['name']
    path = request.form['path']
    extension = request.form['extension']

    song = AudioFile(name, path, extension)

    request_play(song)

    return render_template('play.html', song=song)


app.run(host='127.0.0.1', port=8080, debug=True)
