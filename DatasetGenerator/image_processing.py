#################################################
# Image Processing:                             #
# The image scraper simply downloads the images #
# from the google search. For using it for deep #
# learning, we need to further process them.    #
# This however, is highly depending on your use #
# case, and might completely differ.            #
#################################################

import os
import cv2 as cv
import numpy as np

import DatasetGenerator.utils as utils

PATH_IN = '../data_calligraphy/data'
PATH_OUT = '../data_calligraphy/processed'


def process_images(size=(640, 480)):
    """ Prepare all images in folder for the data set. """
    utils.create_folder(PATH_OUT)
    images = utils.get_file_list(PATH_IN, extension='.jpg')

    for idx, img_name in enumerate(images):
        if idx % 100 == 0:
            print(str(idx) + '/' + str(len(images)))
        img = utils.read_image(PATH_IN, img_name)
        if img is None:
            continue
        img_processed = convert_image(img, size)
        save_image(img_processed, img_name)


def convert_image(img, size):
    """ Process a single image to fit data set standard. """
    img = binarize(img)  # create black and white image
    img = invert(img)  # invert image if background is black
    img = resize(img, size)  # scale image down so it fits in target size
    img = add_background(img, size)  # place image on white background
    return img


def binarize(img):
    """ Create a black and white image with Otsu Binarization. """
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    _, img = cv.threshold(img, 0, 255, cv.THRESH_OTSU)
    return img


def invert(img):
    """ Correct background-foreground assignment:
    Change background to white and foreground to black
    """
    # idea: invert image if more than half the pixels are black
    num_pixels = img.shape[0] * img.shape[1]
    num_white = img.sum() / 255

    if num_white > num_pixels/2:
        return img
    return 255-img


def resize(img, dim_out):
    """ Up / down-size an image. """
    dim_in = img.shape  # height, width, channels
    ratio_in = dim_in[1] / dim_in[0]
    ratio_out = dim_out[1] / dim_out[0]

    # decide whether height or width is the limiting factor for scaling
    if ratio_in > ratio_out:
        scaling_factor = dim_out[1] / dim_in[1]
        new_width = dim_out[1]
        new_height = int(dim_in[0]*scaling_factor)
    else:
        scaling_factor = dim_out[0] / dim_in[0]
        new_width = int(dim_in[1]*scaling_factor)
        new_height = dim_out[0]
    img_resized = cv.resize(img, (new_width, new_height))
    return img_resized


def add_background(img, dim_out):
    """ Places image central on white background. """
    background = np.ones(dim_out) * 255
    if dim_out[0] == img.shape[0]:
        left = int(dim_out[1]/2 - img.shape[1]/2)
        right = left + img.shape[1]
        background[:, left:right] = img
    else:
        top = int(dim_out[0]/2 - img.shape[0]/2)
        bottom = top + img.shape[0]
        background[top:bottom, :] = img
    return background


def save_image(img, name):
    """ Store an image as file. """
    path_img = os.path.join(PATH_OUT, name)
    cv.imwrite(path_img, img)


if __name__ == '__main__':
    image_size = (480, 640)  # height, width to comply with cv2 notation
    process_images(size=image_size)
