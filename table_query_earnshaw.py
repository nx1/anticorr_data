"""
query earnshaw catalogue for swift observations
"""

from source_names import source_names
import numpy as np
import pandas as pd
from astropy.table import Table
from astropy.coordinates import SkyCoord
import astropy.units as u
from astroquery.heasarc import Heasarc
from tqdm import tqdm
from source_names_dict import source_names_dict

source_names = list(source_names_dict.keys())
cat = Table.read('external/Earnshaw_ULX_cat/earnshaw_Xraycatalogue.fits')
cat.sort('SRCID')
print(cat)

source_ids = np.unique(cat['SRCID'])
print(f'Unique source ids in catalogue: {len(source_ids)}')
print('Press any key to start...')
input()

h = Heasarc()


all_summary = []
for id in tqdm(source_ids):
    error = False
    summary = {}
    sub = cat[cat['SRCID'] == id]
    ra, dec = sub[0]['RA'], sub[0]['DEC']
    sc = SkyCoord(ra, dec, unit=u.deg)
    try:
        tab = h.query_region(position=sc, mission='SWIFTMASTR', radius=23.6*u.arcmin, resultmax=3000)

    except :
        tab = None
        error = True
        
    summary['SRCID'] = id
    summary['RA'] = ra
    summary['DEC'] = dec
    if error:
        summary['n_obs'] = 0
        summary['n_obs_uvot'] = 0
        summary['n_obs_xrt']  = 0
        summary['total_uvot_exp'] = 0
        summary['total_xrt_exp']  = 0
    else:
        summary['n_obs'] = len(tab)
        summary['n_obs_uvot'] = np.count_nonzero(tab['UVOT_EXPOSURE'])
        summary['n_obs_xrt']  = np.count_nonzero(tab['XRT_EXPOSURE'])
        summary['total_uvot_exp'] = tab['UVOT_EXPOSURE'].sum()
        summary['total_xrt_exp']  = tab['XRT_EXPOSURE'].sum()
    all_summary.append(summary)

df_all_summary = pd.DataFrame(all_summary).sort_values('n_obs', ascending=False)
print(df_all_summary)
n_obs_tot = df_all_summary["n_obs"].sum()
print(f'Total obs={n_obs_tot} \t estimated size = {0.025*n_obs_tot} gb')

savedir = 'tables/earnshaw_summary.csv' 
print(f'savings results to: {savedir}')
df_all_summary.to_csv(savedir, index=False)

