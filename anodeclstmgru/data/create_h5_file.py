import anodeclstmgru.constants as const
import pandas as pd


def transform_time_stamp(df):
    df['Timestamp'] = pd.to_datetime(df[' Timestamp'])
    df = df.drop(' Timestamp', axis=1)
    return df


def run():
    paths = const.PHYS_NORMAL_PATHS + [const.PHYS_ATTACK_PATH]
    names = ['df_labels', 'df_phys_norm_v0', 'df_phys_norm_v1',
             'df_phys_att_v0']
    store = pd.HDFStore(const.HDF_STORE_PATH)
    df_labels = pd.read_excel(const.LABELS_FILE_PATH)
    store['df_labels'] = df_labels
    for path, name in zip(paths, names):
        df = pd.read_excel(path, header=1)
        df = transform_time_stamp(df)
        store[name] = df
    store.close()


if __name__ == '__main__':
    breakpoint()
    run()
