import pickle

from flask import Flask, render_template, url_for, request, redirect
import socket

from audio_file import AudioFile

app = Flask(__name__)

server_address = socket.gethostname()
server_port = 12000
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HEADER_SIZE = 10

client_socket.connect((socket.gethostname(), server_port))


def fetch_library_songs():
    while True:
        msg_len = 0
        full_msg = b''
        new_msg = True

        while True:
            msg = client_socket.recv(16)

            if new_msg:
                msg_len = int(msg[:HEADER_SIZE])
                new_msg = False

            full_msg += msg

            if len(full_msg) - HEADER_SIZE == msg_len:
                return pickle.loads(full_msg[HEADER_SIZE:])


@app.route('/')
def index():
    library = fetch_library_songs()
    return render_template('library.html', title="library", library=library)


@app.route('/play/<string:song>')
def play(song):
    return render_template('play.html', song=song)


@app.route('/play_song', methods=['POST', ])
def play_song():
    name = request.form['name']
    path = request.form['path']
    extension = request.form['extension']

    song = AudioFile(name, path, extension)

    return render_template('play.html', song=song)


app.run(host='127.0.0.1', port=8080, debug=True)
