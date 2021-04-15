import pytorch_lightning as pl
import torch
from torch import nn
from pytorch_lightning.metrics import MeanAbsoluteError as MSE


class LSTMEncoder(torch.nn.Module):
    def __init__(self, input_size: int = 51, hidden_size: int = 128,
                 embedding_size: int = 64):
        super(LSTMEncoder, self).__init__()
        self.layer1 = nn.LSTM(input_size=input_size, batch_first=True,
                              hidden_size=hidden_size).float()
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
                 embedding_size: int = 64, seq_len: int = 100):
        super(LSTMDecoder, self).__init__()
        self.layer1 = nn.LSTM(input_size=embedding_size, batch_first=True,
                              hidden_size=hidden_size).float()
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

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.encoder = LSTMEncoder()
        self.decoder = LSTMDecoder()
        self.metric = MSE()

    def forward(self, x):
        return self.encoder(x)

    def training_step(self, batch, batch_idx):
        x = batch
        embedding = self.encoder(x)
        x_hat = self.decoder(embedding)
        loss = self.metric(x, x_hat)
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
        self.log(f'{prefix}_loss', loss)

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
        return optimizer
