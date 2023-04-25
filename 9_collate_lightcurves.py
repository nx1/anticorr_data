from glob import glob
import numpy as np

import pandas as pd
from astropy.table import Table, unique
import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.table import vstack, hstack, join, unique
from astropy.units import UnitsWarning
from astroquery.simbad import Simbad


import warnings
from source_names_dict import source_names_dict
from table_closest_srcreg import get_src_region_dict

warnings.filterwarnings('ignore', category=UnitsWarning, append=True)

# Fix glob square bracket issue
to_replace = {'[':'[[]',
              ']':'[]]'}

# Associate Source files with nearsest SIMBAD ID
src_region_dict = get_src_region_dict()

print('='*60)

col_names = ['SIMBAD_ID', 'LOCAL_ID', 'N_UVOTSOURCE', 'SRC_REG']
print(f'{col_names[0]:<30} {col_names[1]:<20} {col_names[2]:<12} {col_names[3]:<10}')

all_lcs = {}
for simbad_name, local_name in source_names_dict.items():
    lcs = {}
    
    src_reg = src_region_dict[simbad_name]
    src_reg_stem = src_reg.split('/')[-1].split('.')[0]+'_'
    
    simbad_name_glob = simbad_name.translate(str.maketrans(to_replace)) # Used to fix globbing square brackets
    
    uvotsource_files = glob(f'/mnt/d/anticorr_data/download_scripts/{local_name}/*uvotsource_all.fits')
    
    all_tables = []

    for fn in uvotsource_files:
        if src_reg_stem in fn:
            tab = Table.read(fn)
            tab = unique(tab, keys='OBSID')
            for f in np.unique(tab['FILTER']):
                sub = tab[tab['FILTER'] == f]
                lcs[f'UVOT_{f}'] = sub

    all_lcs[simbad_name] = lcs
    print(f'{simbad_name:<30} {local_name:<20} {len(uvotsource_files):<12} {src_reg_stem:<10}')
    
for simbad_name, lcs in all_lcs.items():
    for lc_name, tab in lcs.items():
        filename = f'{simbad_name},{lc_name}.fits'
        savepath = f'lightcurves/uvot/{filename}'
        print(f'Saving file to: {savepath}')
        tab.write(savepath, format='fits', overwrite=True)
    
