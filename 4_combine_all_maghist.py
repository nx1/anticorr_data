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
        maghist_files = glob(f'{s}*/*{srcreg}_maghist*')
        maghist_fits = s+f'{srcreg}_maghist_all.fits'
        
        if len(maghist_files) == 0:
            print('No maghist files found')
            continue
        
        if os.path.exists(maghist_fits):
            print(f'{maghist_fits} already exists, skipping...')
            continue


 
        all_tabs = []

        for f in tqdm(maghist_files):
            tab = Table.read(f)
            tab['OBSID'] = re.search(r'\d{11}', f)[0]
            all_tabs.append(tab)

        table = vstack(all_tabs)


        print(f'Saving table to {maghist_fits}')
        table.write(maghist_fits, format='fits')
