import os
import cv2 as cv


def create_folder(path_out, purge=False):
    """ Creates output folder (path_out) if it does not exist. """
    folders = path_out.split('/')

    # create all necessary folders on the path
    for i, folder in enumerate(folders):
        if folder != '..':
            path = os.path.join(*folders[0:i+1])
            if not os.path.exists(path):
                os.mkdir(path)


def get_file_list(path_folder, extension=''):
    """ Lists all files from a folder with an specific file extension. """
    files = []
    for file in os.listdir(path_folder):
        if file.endswith(extension):
            files.append(file)
    return files


def read_image(path, img_name):
    """ Load an image by name"""
    img_path = os.path.join(path, img_name)
    return cv.imread(img_path)
