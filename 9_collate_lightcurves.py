from glob import glob
import numpy as np

import pandas as pd
from astropy.table import Table
import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.table import vstack, hstack, join, unique
from astroquery.simbad import Simbad


from source_names_dict import source_names_dict
from get_closest_srcreg import get_src_region_dict

# Fix glob square bracket issue
to_replace = {'[':'[[]',
              ']':'[]]'}

# Associate Source files with nearsest SIMBAD ID
src_region_dict = get_src_region_dict()

print('='*60)

xrt_colnames1 = ['MJD', 'T_+ve', 'T_-ve', 'Rate', 'Ratepos', 'Rateneg', 'obsID'] # From full band qdp files
xrt_colnames2 = ['MJD', 'Err (pos)', 'Err(neg)', 'Rate', 'Error', 'obsID']       # From soft/hard/hr qdp files

col_names = ['SIMBAD_ID', 'LOCAL_ID', 'N_MAGHIST', 'N_UVOTSOURCE', 'N_CSV', 'SRC_REG']
print(f'{col_names[0]:<30} {col_names[1]:<20} {col_names[2]:<10} {col_names[3]:<12} {col_names[4]:<10} {col_names[5]:<10}')

all_lcs = {}
for simbad_name, local_name in source_names_dict.items():
    lcs = {}
    
    src_reg = src_region_dict[simbad_name]
    src_reg_stem = src_reg.split('/')[-1].split('.')[0]+'_'
    
    
    simbad_name_glob = simbad_name.translate(str.maketrans(to_replace)) # Used to fix globbing square brackets
    
    uvotsource_files = glob(f'/mnt/d/anticorr_data/download_scripts/{local_name}/*uvotsource_all.fits')
    maghist_files    = glob(f'/mnt/d/anticorr_data/download_scripts/{local_name}/*maghist_all.fits*')
    csv_files        = glob(f'/mnt/d/anticorr_data/UKSSDC/{simbad_name_glob}/*/*/*.csv')
    
    all_tables = []
    
    for csv in csv_files:
        tab = Table.from_pandas(pd.read_csv(csv, dtype={'obsID':str}))
        all_tables.append(tab)

        if tab.colnames == xrt_colnames1:
            new_names = ['MJD', 'MJD_ERR_POS', 'MJD_ERR_NEG', 'RATE', 'RATE_ERR_POS', 'RATE_ERR_NEG', 'OBSID']
            tab.rename_columns(xrt_colnames1, new_names)
            tab['RATE_ERR'] = tab['RATE_ERR_POS'] + abs(tab['RATE_ERR_NEG'])
            
        if tab.colnames == xrt_colnames2:
            new_names = ['MJD', 'MJD_ERR_POS', 'MJD_ERR_NEG', 'RATE', 'RATE_ERR', 'OBSID']
            tab.rename_columns(xrt_colnames2, new_names)
            

        if 'curve' in csv:
            key = 'XRT_FULL'
        if 'HARD' in csv:
            key = 'XRT_HARD'
        if 'SOFT' in csv:
            key = 'XRT_SOFT'
        if 'HR' in csv:
            key = 'XRT_HR'
        if 'PC' in csv:
            key += '_PC'
        if 'WT' in csv:
            key += '_WT'
        lcs[key] = tab
        
            

    for maghist in maghist_files:
        if src_reg_stem in maghist:
            # print(src_reg_stem, maghist)
            tab = Table.read(maghist)
            for f in np.unique(tab['FILTER']):
                sub = tab[tab['FILTER'] == f]
                lcs[f'UVOT_{f}'] = sub

    all_lcs[simbad_name] = lcs
    print(f'{simbad_name:<30} {local_name:<20} {len(maghist_files):<10} {len(uvotsource_files):<12} {len(csv_files):<8} {src_reg_stem:<10}')
    
for simbad_name, lcs in all_lcs.items():
    for lc_name, tab in lcs.items():
        filename = f'{simbad_name},{lc_name}.fits'
        savepath = f'lightcurves/{filename}'
        print(f'Saving file to: {savepath}')
        tab.write(savepath, format='fits', overwrite=True)
    
