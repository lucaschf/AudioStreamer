import os

from audio_file import AudioFile


def get_file_extension(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    return ext


def get_audio_files_from_directory(folder):
    extensions = ['wav', ]
    file_names = [fn for fn in os.listdir(folder) if any(fn.endswith(ext) for ext in extensions)]

    files = list()

    for file in file_names:
        files.append(AudioFile(file.lower().title(), folder + "/" + file, get_file_extension(file)))

    return files
