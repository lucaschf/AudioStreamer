import socket
import threading

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

    print("Receiving")

    _format = 8
    channels = 2
    rate = 44100
    chunk = CHUNK

    stream = p_audio.open(format=_format, channels=channels, rate=rate, output=True)

    content = connection.recv(chunk)

    global playing
    playing = True
    while content:
        stream.write(content)  # plays audio
        content = connection.recv(CHUNK)

        if not playing:
            break

    stream.close()
    p_audio.terminate()
    connection.close()


def request_play(song):
    connection = create_connection()

    data = {Action.play_song: song}
    send_data(data, connection)

    receive_and_play_song(connection)

    connection.close()


def request_library():
    sock = create_connection()
    data = {Action.fetch_library: ''}
    send_data(data, sock)

    result = receive_data(sock)
    sock.close()

    return result


@app.route('/')
def index():
    return render_template('library.html', title="library", song="No song playing", library=request_library())


@app.route('/play_song', methods=['POST', ])
def play_song():
    name = request.form['currentSongName']
    path = request.form['currentSongPath']
    extension = request.form['currentSongExt']

    song = Song(name, path, extension)

    global th
    global playing
    playing = False

    th = threading.Thread(target=request_play, args=[song])
    th.start()

    return render_template('library.html', title="library", song=song.name, library=request_library())


@app.route('/stop', methods=['POST', ])
def stop():
    global playing

    playing = False

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='10.0.1.15', port=8080, debug=True)
