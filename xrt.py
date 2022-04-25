from glob import glob
import numpy as np
import pandas as pd
from astropy.table import Table

def load_xrt(simbad_name='NAME_NGC_1313_X-1', curve='PC', pandas=True):
    print(f'Loading XRT...')
    print(f'simbad_name={simbad_name} curve={curve} pandas={pandas}')
    if curve == 'PC':
        s = f'/mnt/d/anticorr_data/UKSSDC/{simbad_name}/*/*/*curve_PC.csv'
    elif curve == 'HARD':
        s = f'/mnt/d/anticorr_data/UKSSDC/{simbad_name}/*/*/*hardrat_HARD_PC.csv'
    elif curve == 'SOFT':
        s = f'/mnt/d/anticorr_data/UKSSDC/{simbad_name}/*/*/*hardrat_SOFT_PC.csv'
    elif curve == 'HR':
        s = f'/mnt/d/anticorr_data/UKSSDC/{simbad_name}/*/*/*hardrat_HR_PC.csv'
        
    csv_file = glob(s)[0]
    print(f'Loading file: {csv_file}')
    df = pd.read_csv(csv_file, dtype={'obsID':str})
    n_unique_obs = len(np.unique(df['obsID']))
    print(f'df shape={df.shape} unique_obs={n_unique_obs}')
    if pandas:
        return df
    else:
        table = Table.from_pandas(df)
        return table

def rename_xrt_cols(Table):
    xrt_colnames1 = ['MJD', 'T_+ve', 'T_-ve', 'Rate', 'Ratepos', 'Rateneg', 'obsID']
    xrt_colnames1_new = ['MJD', 'MJD_ERR_POS', 'MJD_ERR_NEG', 'RATE', 'RATE_ERR_POS', 'RATE_ERR_NEG', 'OBSID']
    xrt_colnames2 = ['MJD', 'Err (pos)', 'Err(neg)', 'Rate', 'Error', 'obsID']       # From soft/hard/hr qdp files
    xrt_colnames2_new = ['MJD', 'MJD_ERR_POS', 'MJD_ERR_NEG', 'RATE', 'RATE_ERR', 'OBSID']       # From soft/hard/hr qdp files
    
    if list(Table.columns) == xrt_colnames1:
        Table.rename_columns(xrt_colnames1, xrt_colnames1_new)
    elif list(Table.columns) == xrt_colnames2:
        Table.rename_columns(xrt_colnames2, xrt_colnames2_new)
    else:
        print('Table columns not recognized!')
    return Table
    

if __name__ == "__main__":
    df = load_xrt(simbad_name='NAME_NGC_1313_X-1', curve='PC', pandas=True)