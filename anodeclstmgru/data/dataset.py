from torch.utils.data import Dataset
import pandas as pd
import numpy as np
import anodeclstmgru.constants as const
from sklearn.preprocessing import StandardScaler


class SWaTSDataset(Dataset):
    """Write me!"""

    def __init__(self, normal: bool = True, window_size: int = 100,
                 sample_size: int = 100, sample_freq: str = None,
                 test_set_step_size: int = 10,
                 *args, **kwargs):
        store = pd.HDFStore(const.HDF_STORE_PATH_PREPROC)
        df_key = 'df_norm' if normal else 'df_att'
        self.df = store[df_key]
        if sample_freq:
            self.df = self.df.resample(sample_freq).mean()
        store.close()
        scaler = StandardScaler()
        self.df.loc[:, const.SENSOR_COLS] = \
            scaler.fit_transform(self.df[const.SENSOR_COLS])
        self.window_size = window_size
        self.sample_size = sample_size
        self.normal = normal
        self.test_set_step_size = test_set_step_size
        self.samples = self._create_samples()

    def _create_samples(self):
        if self.normal:
            # create random number between 0 and len(df) - window size
            start_idx_max = len(self.df) - self.window_size
            start_idxs = np.random.randint(0, start_idx_max, self.sample_size)
            df = self.df.reset_index()[const.SENSOR_COLS]
            return np.array(
                [df.loc[i:i+self.window_size-1].values.astype(np.float32)
                 for i in start_idxs])
        else:
            # create self.sample_size equally sized time windows
            end_idxs = list(range(self.window_size, len(self.df),
                            self.test_set_step_size))
            df = self.df.dropna(how='any')
            df = df.reset_index()
            self.timestamps = list(df.loc[end_idxs, 'Timestamp'].values)
            return np.stack([df.loc[i+1-self.window_size:i][
                const.SENSOR_COLS].values.astype(np.float32)
                             for i in end_idxs])

    def __len__(self):
        """Size of dataset"""
        return self.samples.shape[0]

    def __getitem__(self, index):
        """Get one sample"""
        return self.samples[index, :, :]


if __name__ == '__main__':
    # ds_att = SWaTSDataset(normal=False)
    # ds_norm = SWaTSDataset(sample_size=1000, window_size=200)
    # ds_norm_sample = SWaTSDataset(sample_size=1000, window_size=200,
                                  # sample_freq='60s')
    # sample = ds_norm.__getitem__(10)

    ds_att = SWaTSDataset(
            normal=False, window_size=500,
            sample_size=1000, sample_freq='10s',
            test_set_step_size=100)


    breakpoint()
