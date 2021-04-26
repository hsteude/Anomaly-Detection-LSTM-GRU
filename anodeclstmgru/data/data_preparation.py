# This module performs some basic data preparation steps
import pandas as pd
import anodeclstmgru.constants as const
from anodeclstmgru.data.create_h5_file import run as create_data_store
import os


class DataCleaner():
    def __init__(self):
        self.in_store = pd.HDFStore(const.HDF_STORE_PATH_INTERIM)
        self.out_store = pd.HDFStore(const.HDF_STORE_PATH_PREPROC)
        if not os.path.isfile(const.HDF_STORE_PATH_INTERIM):
            create_data_store()

    def _close_data_stores(self):
        self.in_store.close()
        self.out_store.close()

    def _read_dfs(self):
        df_norm = self.in_store['df_phys_norm_v1']
        df_att = self.in_store['df_phys_att_v0']
        df_labels = self.in_store['df_labels']
        return df_norm, df_att, df_labels

    @staticmethod
    def _to_timeseries(dfs: list) -> list:
        out = []
        for df in dfs:
            df['Timestamp'] = pd.to_datetime(df[' Timestamp'])
            df = df.drop(' Timestamp', axis=1)
            df = df.set_index('Timestamp', drop=True)
            out.append(df)
        return out

    @staticmethod
    def _fix_column_names(dfs: list) -> list:
        """There were a lot of colnames starting with white spaces"""
        for df in dfs:
            df.columns = [s.replace(' ', '') for s in df.columns]
        return dfs

    @staticmethod
    def _filter_time_window(dfs: list) -> list:
        """There was a bug (i think) in the data. See exploration notebook"""
        return [df[(df.index > const.MIN_DATE)
                   & (df.index < const.MAX_DATE)].copy() for df in dfs]

    @staticmethod
    def _clean_attack_column(dfs: list) -> list:
        for df in dfs:
            df.loc[df['Normal/Attack'] == 'A ttack',
                   'Normal/Attack'] = 'Attack'
        return dfs

    def _store_dfs(self, dfs: list):
        for df, key in zip(dfs, ['df_norm', 'df_att']):
            self.out_store[key] = df

    def preprocess(self):
        df_norm, df_att, df_labels = self._read_dfs()
        df_norm, df_att = self._to_timeseries([df_norm, df_att])
        df_norm, df_att = self._fix_column_names([df_norm, df_att])
        df_norm, df_att = self._filter_time_window([df_norm, df_att])
        df_norm, df_att = self._clean_attack_column([df_norm, df_att])
        self._store_dfs([df_norm, df_att])
        self._close_data_stores()


if __name__ == '__main__':
    dpr = DataCleaner()
    dpr.preprocess()
