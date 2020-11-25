import os
import glob

from audio_file import AudioFile


def get_files(dir_name):
    list_of_file = os.listdir(dir_name)
    complete_file_list = list()

    for file in list_of_file:
        complete_path = os.path.join(dir_name, file)

        if os.path.isdir(complete_path):
            complete_file_list = complete_file_list + get_files(complete_path)
        else:
            complete_file_list.append(complete_path)

    return complete_file_list


def get_files2(dir_name):
    files = [f for f in glob.glob(dir_name, recursive=True)]

    return files


def get_files3(folder_path, extensions):
    file_names = [fn for fn in os.listdir(folder_path)
                  if any(fn.endswith(ext) for ext in extensions)]

    return file_names


def get_file_extension(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    return ext


def get_audio_from_directory(folder):
    extensions = ['mp3', 'wav']
    file_names = [fn for fn in os.listdir(folder) if any(fn.endswith(ext) for ext in extensions)]

    files = list()

    for file in file_names:
        files.append(AudioFile(file.lower().title(), folder + "/" + file, get_file_extension(file)))

    return files


def get_audio_files_from_directory(folder):
    extensions = ['mp3', 'wav']
    file_names = [fn for fn in os.listdir(folder) if any(fn.endswith(ext) for ext in extensions)]

    return file_names
