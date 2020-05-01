import os
import utils
import random
import shutil


path_in = '../data_calligraphy'
path_out = '../data_calligraphy/split'


def split_set(sources, ratios, split_names):
    """ Split a data set into multiple random sets.

    sources: list of input folder names that need to be splitted to equally named folders
    ratios: list of ratios for each part of the split
    split_names: name of the split folders e.g. train, val, test
    """
    if sum(ratios) != 1:
        print('Invalid ratios')
        return
    if len(ratios) != len(split_names):
        print('Invalid names')
    for source in sources:
        split_source(source, ratios, split_names)


def split_source(source, ratios, folder_names):
    """ See split_set(), but for a single source. """
    create_folders(folder_names, source)
    file_list = os.listdir(os.path.join(path_in, source))
    random.shuffle(file_list)
    file_idx = 0
    for j, name in enumerate(folder_names):
        while file_idx < len(file_list)*sum(ratios[:j+1]):
            copy_file(source, file_list[file_idx], name)
            file_idx += 1


def copy_file(source, file_name, folder_name):
    """ Copy a file to new split destination. """
    path_old = os.path.join(path_in, source, file_name)
    path_new = os.path.join(path_out, folder_name, source, file_name)
    shutil.copy(path_old, path_new)


def create_folders(folder_names, suffix):
    """ Create new folder for the output data. """
    for folder in folder_names:
        path = os.path.join(path_out, folder, suffix)
        utils.create_folder(path, purge=True)


if __name__ == '__main__':
    split_set(['normal', 'cal'], [0.8, 0.2], ['train', 'val'])
