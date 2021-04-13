import anodeclstmgru.constants as const
import pandas as pd


def excel_to_df(path):
    return pd.read_excel(path, header=1)


def transform_time_stamp(df):
    df['Timestamp'] = pd.to_datetime(df[' Timestamp'])
    df = df.drop(' Timestamp', axis=1)
    return df


def store_to_h5(df, store, key,):
    store[key] = df


if __name__ == '__main__':
    breakpoint()
    paths = const.PHYS_NORMAL_PATHS + [const.PHYS_ATTACK_PATH]
    names = ['df_phys_norm_v0', 'df_phys_norm_v1', 'df_phys_att_v0']
    store = pd.HDFStore(const.HDF_STORE_PATH)
    for path, key in zip(paths, names):
        df = excel_to_df(path)
        df = transform_time_stamp(df)
        store_to_h5(df, store, key)
    store.close()
