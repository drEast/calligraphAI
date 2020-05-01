#################################################
# Manual Check                                  #
# Although the scraper and image processing     #
# yield good results, it is not 100% perfect.   #
# This is mainly due to falsely labelled images #
# by the search, or the creation of binary      #
# images. Therefore, this is used to go manually#
# traverse the data set and filter out bad s    #
# samples fast.                                 #
#################################################

import os
import shutil
import cv2 as cv
import matplotlib.pyplot as plt

import utils as utils

PATH_IN = '../data_calligraphy/processed'
PATH_OUT_POS = '../data_calligraphy/filtered/good'
PATH_OUT_NEG = '../data_calligraphy/filtered/bad'


class Checker:
    """ Class encapsulation for communicating information to click event. """
    def __init__(self):
        self.keys_accept = [' ']
        self.image_names = utils.get_file_list(PATH_IN)
        self.idx = 0
        self.next = True

    def start_check(self):
        """ Sorts images by keyboard input. """
        utils.create_folder(PATH_OUT_NEG, purge=True)
        utils.create_folder(PATH_OUT_POS, purge=True)

        fig, _ = plt.subplots()
        fig.canvas.mpl_connect('key_press_event', self.keyboard_event)
        plt.axis('off')

        while self.idx != len(self.image_names):
            if self.next:
                self.show_image()
            #time.sleep(10)

    def keyboard_event(self, event):
        """ Copy file to folder depending on pressed key. """
        if event.key in self.keys_accept:
            folder = PATH_OUT_POS
        else:
            folder = PATH_OUT_NEG

        file_name_new = os.path.join(folder, self.image_names[self.idx])
        file_name_old = os.path.join(PATH_IN, self.image_names[self.idx])
        shutil.copy(file_name_old, file_name_new)

        self.idx += 1
        self.next = True

    def show_image(self):
        """ Displays the next image. """
        self.next = False
        img = cv.imread(os.path.join(PATH_IN, self.image_names[self.idx]))
        plt.imshow(img)
        plt.show(block=False)


if __name__ == '__main__':
    manual_checker = Checker()
    manual_checker.start_check()
