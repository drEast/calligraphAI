import os
import shutil


def create_folder(path_out, purge=False):
    """ Creates output folder (path_out) if it does not exist. """
    path_out = path_out.replace('\\', '/')
    folders = path_out.split('/')

    # create all necessary folders on the path
    for i, folder in enumerate(folders):
        if folder != '..':
            path = os.path.join(*folders[0:i+1])
            if not os.path.exists(path):
                os.mkdir(path)
    if purge:
        shutil.rmtree(path_out)
        os.mkdir(path_out)


def get_file_list(path_folder, extension=''):
    """ Lists all files from a folder with an specific file extension. """
    files = []
    for file_name in os.listdir(path_folder):
        if file_name.endswith(extension):
            files.append(file_name)
    return files

