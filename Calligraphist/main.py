import Calligraphist.Dataloader
import Calligraphist.Model
import Calligraphist.Trainer


config = {
    'paths': {
        'data_train': '../data_calligraphy/split/train',
        'data_val': '../data_calligraphy/split/val',
        'samples': '../samples'
    },
    'training': {
        'epochs': 100,
        'batch_train': 16,
        'batch_val': 16,
    }
}


def train():
    data_train = Calligraphist.Dataloader.GANLoader(config['paths']['data_train'], config['training']['batch_train'])
    data_val = Calligraphist.Dataloader.GANLoader(config['paths']['data_val'], config['training']['batch_val'])

    model = Calligraphist.Model.GANModel(config)

    training = Calligraphist.Trainer.GANTrainer(config, data_train, data_val, model)
    training.start_training()


if __name__ == '__name__':
    train()
