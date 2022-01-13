from glob import glob
import re

from astropy.table import Table, vstack
from tqdm import tqdm

source_dirs = glob('download_scripts/*/')

for s in source_dirs:
    print(f'Doing {s}')
    maghist_files = glob(f'{s}*/*maghist*')
    if len(maghist_files) == 0:
        print('No maghist files found')
        continue
    all_tabs = []

    for f in tqdm(maghist_files):
        tab = Table.read(f)
        tab['OBSID'] = re.search(r'\d{11}', f)[0]
        all_tabs.append(tab)

    table = vstack(all_tabs)

    maghist_fits = s+'maghist_all.fits'
    print(f'Saving table to {maghist_fits}')
    table.write(maghist_fits, format='fits')

