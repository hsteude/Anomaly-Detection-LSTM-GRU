import pytorch_lightning as pl
from torch.utils.data import DataLoader, random_split
from anodeclstmgru.data.dataset import SWaTSDataset


class SWaTSDataModule(pl.LightningDataModule):

    def __init__(self, batch_size: int = 32, window_size: int = 100,
                 sample_size: int = 100, sample_freq: str = None,
                 validation_split: float = 0.05):
        super().__init__()
        self.batch_size = batch_size
        self.window_size = window_size
        self.sample_size = sample_size
        self.sample_freq = sample_freq
        self.validation_split = validation_split

    def setup(self, stage=None):
        self.swats_test = SWaTSDataset(
            normal=False, window_size=self.window_size,
            sample_size=self.sample_size, sample_freq=self.sample_freq)
        swat_full = SWaTSDataset(
            normal=True, window_size=self.window_size,
            sample_size=self.sample_size, sample_freq=self.sample_freq)
        train_length = int(self.validation_split * len(swat_full))
        val_length = len(swat_full) - train_length
        self.swats_train, self.swats_val = random_split(
            swat_full, [train_length,  val_length])

    def train_dataloader(self):
        return DataLoader(self.swats_train, batch_size=self.batch_size)

    def val_dataloader(self):
        return DataLoader(self.swats_val, batch_size=self.batch_size)

    def test_dataloader(self):
        return DataLoader(self.swats_test, batch_size=self.batch_size)
