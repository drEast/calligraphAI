import tensorflow as tf

import Calligraphist.Architecture


class GANModel:

    def __init__(self, config):
        self.config = config

        self.generator = Calligraphist.Architecture.load_generator()
        self.discriminator = Calligraphist.Architecture.load_discriminator()

        self.generator_loss = self.load_gen_loss()
        self.discriminator_loss = self.load_dis_loss()

    def load_gen_loss(self):
        tf

    def load_dis_loss(self):
        return 0
