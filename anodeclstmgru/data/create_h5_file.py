import anodeclstmgru.constants as const
import pandas as pd
from loguru import logger


def run():
    logger.info('Converting excel files to h5 data store. '
                'This will take a while')
    paths = const.PHYS_NORMAL_PATHS + \
        [const.PHYS_ATTACK_PATH] + [const.LABELS_FILE_PATH]
    names = ['df_phys_norm_v0', 'df_phys_norm_v1',
             'df_phys_att_v0', 'df_labels']
    store = pd.HDFStore(const.HDF_STORE_PATH_INTERIM)
    for path, name in zip(paths, names):
        header = 0 if name == 'df_labels' else 1
        df = pd.read_excel(path, header=header)
        store[name] = df
        logger.info(f'Stored {name} in data store')
    store.close()


if __name__ == '__main__':
    run()
