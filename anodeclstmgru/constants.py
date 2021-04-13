import os

# PATHS
DATA_FOLDER_PATH = os.path.join('.', 'data', 'interim',
                                'SWaT.A1 _ A2_Dec 2015')
PHYSICAL_FOLDER_PATH = os.path.join(DATA_FOLDER_PATH, 'Physical')
NETWORK_FOLDER_PATH = os.path.join(DATA_FOLDER_PATH, 'NETWORK')
LABELS_FILE_PATH = os.path.join(DATA_FOLDER_PATH, 'List_of_attacks_Final.xlsx')
PHYS_NORMAL_PATHS = [
    os.path.join(PHYSICAL_FOLDER_PATH, f)
    for f in ['SWaT_Dataset_Normal_v0.xlsx', 'SWaT_Dataset_Normal_v1.xlsx']]
HDF_STORE_PATH = os.path.join(DATA_FOLDER_PATH, 'data_store.h5')
