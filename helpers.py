import os

from song import Song


def get_file_extension(file_path):
    ext = os.path.splitext(file_path)[-1].lower().strip()
    return ext


def __file_name_no_extension(file_name):
    pos = file_name.rfind('.')
    return file_name[:pos]


def get_audio_files_from_directory(folder):
    extensions = ['wav', 'mp3']
    file_names = [fn for fn in os.listdir(folder) if any(fn.endswith(ext) for ext in extensions)]

    files = list()

    for file in file_names:
        name = __file_name_no_extension(file)
        files.append(Song(name.lower().title(), folder + "/" + file, get_file_extension(file)))

    return files
