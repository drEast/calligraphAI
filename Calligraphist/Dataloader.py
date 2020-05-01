import tensorflow as tf

import os


def load(path_image):
    img = tf.io.read_file(path_image)
    img = tf.image.decode_jpeg(img)
    img = tf.cast(img, tf.float32)
    return img


class GANLoader:

    def __init__(self, folder, batch_size):
        self.folder_nor = os.path.join(folder, 'normal')
        self.folder_cal = os.path.join(folder, 'cal')
        self.batch_size = batch_size
        self.iterator = self.build_set()

    def build_set(self):
        data = self.image_names()
        data = data.map(load, num_parallel_calls=1)
        data = data.batch(self.batch_size, drop_remainder=True)
        data = data.prefetch(1)
        iterator = data.make_initializable_iterator()
        return iterator

    def image_names(self):
        files_normal = tf.data.Dataset.list_files(self.folder_nor + '*')
        files_normal.shuffle()

        files_calligraphy = tf.data.Dataset.list_files(self.folder_cal + '*')
        files_calligraphy.shuffle()

        files_combined = files_normal.interleave(
            lambda x: files_calligraphy, cycle_length=self.batch_size, block_length=1)
        return files_combined
