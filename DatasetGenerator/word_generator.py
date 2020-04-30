from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from bidi.algorithm import get_display
import arabic_reshaper

import random
import os
import utils


def create_set(path, amount):
    """ Store [amount] images of random arabic text to [path]. """
    utils.create_folder(path, purge=True)

    for idx in range(amount):
        text = random_text()
        image = text_2_image(text)
        save_image(image, path, idx)

        if idx % 50 == 0:
            print(str(idx) + '/' + str(amount))


def random_text(min_len=3, max_len=7):
    """ Get a random text in arabic font.

    min_len: minimal amount of letters
    max_len: maximal amount of letters
    """
    amount_letters = random.randint(min_len, max_len)
    letters = []

    for _ in range(amount_letters):
        letter = random_letter()
        letters.append(letter)

    if random.randint(1, 3) == 1:
        letters[-1] = 'ة'  # A lot of female names end with the letter ta marbuta.
    return ''.join(letters)


def random_letter():
    """ Provides an random arabic letter. """
    forbidden_letters = [ord('ة')]
    unicode = random.randint(ord('ا'), ord('ي'))
    while unicode in forbidden_letters or unicode in range(ord('غ')+1, ord('ف')):
        unicode = random.randint(ord('ا'), ord('ي'))
    letter = chr(unicode)
    return letter


def text_2_image(text, img_size=(640, 480)):
    """ Draws the text on white image of given size. """
    text = arabic_reshaper.reshape(text)
    text = get_display(text)

    font = ImageFont.truetype("arial.ttf", 100)

    img = Image.new('L', img_size, 255)
    draw = ImageDraw.Draw(img)

    text_size = draw.textsize(text, font)
    position = ((img_size[0] - text_size[0])/2, (img_size[1]-text_size[1])/2)
    draw.text(position, text, font=font, fill=0)
    return img


def save_image(image, path, idx):
    """ Save the (PIL) image with unique file name. """
    image_name = str(idx) + '.jpg'
    image_path = os.path.join(path, image_name)
    image.save(image_path)


if __name__ == '__main__':
    output_path = '../data_calligraphy/normal'

    create_set(output_path, amount=1000)
