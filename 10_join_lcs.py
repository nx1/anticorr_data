from glob import glob
import warnings
from pathlib import Path
import pandas as pd
from astropy.table import Table, join, unique
from astropy.units import UnitsWarning

from source_names_dict import source_names_dict, get_simbad_name_glob
from uvot import read_uvotsource

warnings.filterwarnings('ignore', category=UnitsWarning, append=True)


xrt_bands = ['SOFT', 'HARD', 'HR']

joined_savepath = Path('/mnt/d/anticorr_data/lightcurves/joined')


i = 0
for simbad_name, local_name in source_names_dict.items():
    simbad_name_glob = get_simbad_name_glob(simbad_name)
    xrt_files = glob(f'lightcurves/xrt/*{simbad_name_glob}*')
    uvot_files = glob(f'lightcurves/uvot/*{simbad_name_glob}*')
    print(f'{simbad_name:<40} {local_name:<40} xrt={len(xrt_files)} uvot={len(uvot_files)}')

    for uvot_file in uvot_files:
        tab_uvot = read_uvotsource(uvot_file)
        uvot_filter = uvot_file.split(',')[-1].split('_')[-1][:-5]
        for xrt_file in xrt_files:
            xrt_stem = xrt_file.split(',')[-1][:-4]

            print(f'{i:<4} {uvot_file:<70} {xrt_file:<40}')

            tab_xrt = pd.read_csv(xrt_file, dtype={'obsID':str})
            tab_xrt = Table.from_pandas(tab_xrt)
            tab_xrt.rename_column('obsID', 'OBSID')
            if 'hardrat' in xrt_file:
                for band in xrt_bands:
                    print(f'{i:<4} {uvot_file:<70} {xrt_file:<40}')
                    tab_xrt_band = tab_xrt[tab_xrt['BAND'] == band]
                    if (len(tab_uvot) >= 10) and (len(tab_xrt_band) >= 10):
   
                        tab_join = join(tab_uvot, tab_xrt_band, join_type='inner', keys='OBSID')
                        tab_join = unique(tab_join, keys=['OBSID'], keep='first')
                        tab_join.sort('MJD_2')
    
                        join_fn = f'{simbad_name},{uvot_filter},{xrt_stem},{band}.fits'
                        tab_join.write(joined_savepath/join_fn, format='fits', overwrite=True)
    
                        print(f'saving file to {join_fn}')
    
                        print('tab_join')
                        print(tab_join)
                        print(f'{i:<4} {uvot_file:<70} {xrt_file:<40} band={band}')
                        i+=1
            else:
                if (len(tab_uvot) >= 10) and (len(tab_xrt) >= 10):
                    tab_join = join(tab_uvot, tab_xrt, join_type='inner', keys='OBSID')
                    tab_join = unique(tab_join, keys=['OBSID'], keep='first')
                    tab_join.sort('MJD_2')
                    join_fn = f'{simbad_name},{uvot_filter},{xrt_stem}.fits'
                    print('tab_join')
                    print(tab_join)
                    print(f'saving file to {join_fn}')
                    tab_join.write(joined_savepath/join_fn, format='fits', overwrite=True)
                    print(f'{i:<4} {uvot_file:<70} {xrt_file:<40}')

                    i+=1

