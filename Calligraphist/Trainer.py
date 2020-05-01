

class GANTrainer:

    def __init__(self, config, data_train, data_val, model):
        self.config = config

        self.data_train = data_train
        self.data_val = data_val
        self.model = model

    def start_training(self):
        print('--- Training started ---')
        for idx in range(self.config['training']['epochs']):
            results_train = self.run_epoch(training=True)
            results_val = self.run_epoch(training=False)
            results = results_train + results_val
            self.print_progress(results)
        print('--- Training ended ---')

    def run_epoch(self, training=True):
        return 0

    def print_progress(self, results):
        output = 'Epoch ../..: dis_loss: .. gen_loss: .. val_dis: .. val_gen: .. in ..s'
        formatted_output = output.format(results)
        print(formatted_output)
