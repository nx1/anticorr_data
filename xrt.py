import logging
from glob import glob
import numpy as np
import pandas as pd
from astropy.table import Table

from source_names_dict import source_names_dict

curves = ['PC', 'HARD', 'SOFT', 'HR']

curve_rmf = {'PC' : Table.read('../external/swift_rsp/swxpc0to12s6_20130101v014.rmf'),
             'WT' : Table.read('../external/swift_rsp/swxwt0to2s6_20131212v015.rmf')}

# Fix glob square bracket issue
to_replace = {'[':'[[]',
              ']':'[]]'}


def log_flag_summary(Table, flag_col):
    n_flag = np.sum(Table[flag_col])
    excluded_obsids = list(Table[Table[flag_col] == True]['OBSID'])
    logging.debug(f'================================')
    logging.debug(f'{flag_col} SUMMARY')
    logging.debug(f' = {n_flag} / {len(Table)} {n_flag / len(Table) * 100 :.2f}%)')
    logging.debug('Excluded obsids:')
    logging.debug(f'{excluded_obsids}')
    logging.debug(f'================================')

def calc_xrt_flags(Table):
    Table['FLAG_RATE<=0'] = Table['RATE'] <= 0
    Table['FLAG>5STD']    = Table['RATE'] > 5*np.std(Table['RATE'])
    
    flags = ['FLAG_RATE<=0', 'FLAG>5STD']
    for f in flags:
        log_flag_summary(Table, f)
    return Table


def load_xrt(simbad_name='NAME_NGC_1313_X-1', curve='PC', pandas=True):
    simbad_name_glob = simbad_name.translate(str.maketrans(to_replace)) # Used to fix globbing square brackets
    logging.debug(f'================================')

    logging.debug(f'Loading XRT simbad_name={simbad_name} curve={curve} pandas={pandas}')
    if curve == 'PC':
        s = f'/mnt/d/anticorr_data/UKSSDC/{simbad_name_glob}/*/*/*curve_PC.csv'
    elif curve == 'HARD':
        s = f'/mnt/d/anticorr_data/UKSSDC/{simbad_name_glob}/*/*/*hardrat_HARD_PC.csv'
    elif curve == 'SOFT':
        s = f'/mnt/d/anticorr_data/UKSSDC/{simbad_name_glob}/*/*/*hardrat_SOFT_PC.csv'
    elif curve == 'HR':
        s = f'/mnt/d/anticorr_data/UKSSDC/{simbad_name_glob}/*/*/*hardrat_HR_PC.csv'
        
    csv_file = glob(s)[0]
    logging.debug(f'Loading file: {csv_file}')
    df = pd.read_csv(csv_file, dtype={'obsID':str})
    n_unique_obs = len(np.unique(df['obsID']))
    logging.debug(f'df shape={df.shape} unique_obs={n_unique_obs}')
    logging.debug(f'================================')

    if pandas:
        return df
    else:
        table = Table.from_pandas(df)
        table = rename_xrt_cols(table)
        table = calc_xrt_flags(table)
        table = table[~table['FLAG_RATE<=0']]
        table = table[~table['FLAG>5STD']]

        return table

def rename_xrt_cols(Table):
    xrt_colnames1 = ['MJD', 'T_+ve', 'T_-ve', 'Rate', 'Ratepos', 'Rateneg', 'obsID']
    xrt_colnames1_new = ['MJD', 'MJD_ERR_POS', 'MJD_ERR_NEG', 'RATE', 'RATE_ERR_POS', 'RATE_ERR_NEG', 'OBSID']
    xrt_colnames2 = ['MJD', 'Err (pos)', 'Err(neg)', 'Rate', 'Error', 'obsID'] # From soft/hard/hr qdp files
    xrt_colnames2_new = ['MJD', 'MJD_ERR_POS', 'MJD_ERR_NEG', 'RATE', 'RATE_ERR', 'OBSID'] # From soft/hard/hr qdp files
    
    if list(Table.columns) == xrt_colnames1:
        Table.rename_columns(xrt_colnames1, xrt_colnames1_new)
        Table['RATE_ERR'] = Table['RATE_ERR_POS'] - Table['RATE_ERR_NEG']
    elif list(Table.columns) == xrt_colnames2:
        Table.rename_columns(xrt_colnames2, xrt_colnames2_new)
    else:
        print('Table columns not recognized!')
        
    Table['MJD_0'] = Table['MJD'] - np.min(Table['MJD'])
    return Table
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        datefmt='%H:%M:%S',
                        format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s')
    for simbad_name, local_name in source_names_dict.items():
        for curve in curves:
            try:
                tab = load_xrt(simbad_name=simbad_name, curve=curve, pandas=False)
            except Exception as e:
                print(f'{simbad_name} {e}')


