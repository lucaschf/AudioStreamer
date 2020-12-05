import socket
import threading
import time

import pyaudio
from flask import Flask, render_template, request, redirect, url_for

from action import Action
from socket_helpers import receive_data, send_data, server_port, server_address, CHUNK
from song import Song

app = Flask(__name__)

global playing
global th


def create_connection():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_address, server_port))
    return sock


def receive_and_play_song(connection):
    p_audio = pyaudio.PyAudio()

    _format = 8
    channels = 2
    rate = 44100

    stream = p_audio.open(format=_format, channels=channels, rate=rate, output=True)

    content = connection.recv(CHUNK)

    global playing
    playing = True

    while content and playing:
        stream.write(content)  # plays audio
        content = connection.recv(CHUNK)

    stream.close()
    p_audio.terminate()
    connection.close()


def play(song):
    connection = create_connection()

    data = {Action.play_song: song}
    send_data(data, connection)

    receive_and_play_song(connection)

    connection.close()


def fetch_library():
    sock = create_connection()
    data = {Action.fetch_library: ''}
    send_data(data, sock)

    result = receive_data(sock)
    sock.close()

    return result


@app.route('/')
def index():
    return render_template('library.html', title="library", library=fetch_library())


@app.route('/play', methods=['POST', ])
def play_song():
    global playing
    playing = False

    name = request.form['currentSongName']
    path = request.form['currentSongPath']
    extension = request.form['currentSongExt']

    song = Song(name, path, extension)

    global th
    th = threading.Thread(target=play, args=[song])

    time.sleep(0.2)
    th.start()

    return render_template('library.html', title="library", song_name=song.name, library=fetch_library())


@app.route('/stop', methods=['POST', ])
def stop():
    global playing

    playing = False

    return redirect(url_for('index'))


if __name__ == '__main__':
    # como o trabalho consiste em comunicações entre sockets, este webclient deve ser rodado apenas no localHost.
    app.run(host='127.0.0.1', port=8080, debug=True)
