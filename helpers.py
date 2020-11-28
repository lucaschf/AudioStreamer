import os

from song import Song


def __get_file_extension(file_path):
    ext = os.path.splitext(file_path)[-1].lower().strip()
    return ext


def __file_name_no_extension(file_name):
    pos = file_name.rfind('.')
    return file_name[:pos]


def get_song_library(folder):
    extensions = ['wav', 'mp3']
    file_names = [fn for fn in os.listdir(folder) if any(fn.endswith(ext) for ext in extensions)]

    songs = list()

    for file in file_names:
        name = __file_name_no_extension(file)
        songs.append(Song(name.lower().title(), folder + "/" + file, __get_file_extension(file)))

    return songs
