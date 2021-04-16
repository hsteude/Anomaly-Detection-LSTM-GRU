import pytorch_lightning as pl
import torch
from torch import nn
from pytorch_lightning.metrics import MeanAbsoluteError as MSE


class LSTMEncoder(torch.nn.Module):
    def __init__(self, input_size: int = 51, hidden_size: int = 128,
                 embedding_size: int = 64, num_lstm_layer: int = 1,
                 *args, **kwargs):
        super(LSTMEncoder, self).__init__()
        self.layer1 = nn.LSTM(input_size=input_size, batch_first=True,
                              hidden_size=hidden_size,
                              num_layers=num_lstm_layer).float()
        self.layer2 = nn.LSTM(input_size=hidden_size, batch_first=True,
                              hidden_size=embedding_size).float()
        self.embedding_size = embedding_size

    def forward(self, x: torch.tensor) -> torch.tensor:
        # x.shape is (batch, seq_len, input_size)
        x, (_, _) = self.layer1(x)
        x, (embedding, _) = self.layer2(x)
        # the embedding shape is (seq_len[in this case 1], batch, input_size)
        # we return in the shape we are used to (batch, seq_len, input_size)
        return embedding.reshape(-1, 1, self.embedding_size)


class LSTMDecoder(torch.nn.Module):
    def __init__(self, input_size: int = 51, hidden_size: int = 128,
                 embedding_size: int = 64, num_lstm_layer: int = 1,
                 seq_len: int = 100, *args, **kwargs):
        super(LSTMDecoder, self).__init__()
        self.layer1 = nn.LSTM(input_size=embedding_size, batch_first=True,
                              hidden_size=hidden_size,
                              num_layers=num_lstm_layer).float()
        self.layer2 = nn.LSTM(input_size=hidden_size, batch_first=True,
                              hidden_size=input_size).float()
        self.seq_len = seq_len

    def forward(self, x: torch.tensor) -> torch.tensor:
        # so x has the shape (batch, seq_lwn, input_size)
        x = x.repeat(1, self.seq_len, 1)
        x, (_, _) = self.layer1(x)
        x, (_, _) = self.layer2(x)
        return x


class AutoEncoderLitModule(pl.LightningModule):

    @staticmethod
    def add_model_specific_args(parent_parser):
        parser = parent_parser.add_argument_group("AutoEncoderLitModule")
        parser.add_argument('--learning_rate', type=float, default=1e-3)
        parser.add_argument('--hidden_size', type=int, default=64)
        parser.add_argument('--embedding_size', type=int, default=128)
        parser.add_argument('--num_lstm_layer', type=int, default=1)
        return parent_parser

    def __init__(self, *args, **kwargs):
        super().__init__()
        # self.hparams is available only after 'save_hyperparameters' is called
        self.save_hyperparameters()
        self.encoder = LSTMEncoder(**self.hparams)
        self.decoder = LSTMDecoder(**self.hparams)
        self.metric = MSE()

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x

    def training_step(self, batch, batch_idx):
        x = batch
        embedding = self.encoder(x)
        x_hat = self.decoder(embedding)
        loss = self.metric(x, x_hat)
        self.logger.experiment.add_scalars("losses", {"train_loss": loss})

        return loss

    def validation_step(self, batch, batch_idx):
        self._shared_eval(batch, batch_idx, 'val')

    def test_step(self, batch, batch_idx):
        self._shared_eval(batch, batch_idx, 'test')

    def _shared_eval(self, batch, batch_idx, prefix):
        x = batch
        embedding = self.encoder(x)
        x_hat = self.decoder(embedding)

        loss = self.metric(x, x_hat)
        self.logger.experiment.add_scalars("losses", {f'{prefix}_loss': loss})

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(),
                                     lr=self.hparams.learning_rate)
        return optimizer
