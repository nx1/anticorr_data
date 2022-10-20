import os
from glob import glob
import re
import warnings

from astropy.units import UnitsWarning
from astropy.table import Table, vstack
from tqdm import tqdm

warnings.filterwarnings('ignore', category=UnitsWarning, append=True)


source_dirs = glob('download_scripts/*/')

for s in source_dirs[1:]:
    print(f'Doing {s}')
    src_reg_files = glob(f'{s}*src*.reg')

    for src in src_reg_files:
        srcreg = src.split('/')[-1][:-4]
        uvotsource_files = glob(f'{s}*/*{srcreg}_uvotsource*')
        uvotsource_fits = s+f'{srcreg}_uvotsource_all.fits'
        
        if len(uvotsource_files) == 0:
            print('No uvotsource files found')
            continue
        
        if os.path.exists(uvotsource_fits):
            print(f'{uvotsource_fits} already exists, skipping...')
            continue


 
        all_tabs = []

        for f in tqdm(uvotsource_files):
            tab = Table.read(f)
            # Get rid of meta info
            tab.meta['HISTORY'] = ''
            tab.meta['comments'] = ''
            tab.meta['COMMENT'] = ''

            tab['OBSID'] = re.search(r'\d{11}', f)[0]
            all_tabs.append(tab)

        table = vstack(all_tabs)


        print(f'Saving table to {uvotsource_fits}')
        table.write(uvotsource_fits, format='fits')
