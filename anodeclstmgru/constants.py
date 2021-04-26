import os
from datetime import datetime

# PATHS
INTERIM_DATA_FOLDER_PATH = os.path.join('.', 'data', 'interim')
PREPROC_DATA_FOLDER = os.path.join('.', 'data', 'processed')
PHYSICAL_FOLDER_PATH = os.path.join(INTERIM_DATA_FOLDER_PATH, 'Physical')
NETWORK_FOLDER_PATH = os.path.join(INTERIM_DATA_FOLDER_PATH, 'NETWORK')
LABELS_FILE_PATH = os.path.join(INTERIM_DATA_FOLDER_PATH,
                                'List_of_attacks_Final.xlsx')
PHYS_NORMAL_PATHS = [
    os.path.join(PHYSICAL_FOLDER_PATH, f)
    for f in ['SWaT_Dataset_Normal_v0.xlsx', 'SWaT_Dataset_Normal_v1.xlsx']]
PHYS_ATTACK_PATH = os.path.join(
    PHYSICAL_FOLDER_PATH, 'SWaT_Dataset_Attack_v0.xlsx')
HDF_STORE_PATH_INTERIM = os.path.join(INTERIM_DATA_FOLDER_PATH,
                                      'data_store.h5')
HDF_STORE_PATH_PREPROC = os.path.join(PREPROC_DATA_FOLDER, 'data_store.h5')

MIN_DATE = datetime(2015, 12, 22)
MAX_DATE = datetime(2016, 1, 2)


# Column names and stuff
SENSOR_COLS = ['FIT101',
               'LIT101',
               'MV101',
               'P101',
               'P102',
               'AIT201',
               'AIT202',
               'AIT203',
               'FIT201',
               'MV201',
               'P201',
               'P202',
               'P203',
               'P204',
               'P205',
               'P206',
               'DPIT301',
               'FIT301',
               'LIT301',
               'MV301',
               'MV302',
               'MV303',
               'MV304',
               'P301',
               'P302',
               'AIT401',
               'AIT402',
               'FIT401',
               'LIT401',
               'P401',
               'P402',
               'P403',
               'P404',
               'UV401',
               'AIT501',
               'AIT502',
               'AIT503',
               'AIT504',
               'FIT501',
               'FIT502',
               'FIT503',
               'FIT504',
               'P501',
               'P502',
               'PIT501',
               'PIT502',
               'PIT503',
               'FIT601',
               'P601',
               'P602',
               'P603']
ATTACK_COL = ['Normal/Attack']
