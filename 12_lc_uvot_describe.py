from glob import glob
import numpy as np
import pandas as pd
from source_names_dict import source_names_readable
from astropy.table import Table

from astropy.units import UnitsWarning
import warnings
warnings.filterwarnings('ignore', category=UnitsWarning, append=True)


uvot_lightcurves = glob('lightcurves/uvot/*fits')
print(f'Found {len(uvot_lightcurves)} uvot lightcurves')

def analyse_uvot_lc(lc):
    print(lc)
    sp = lc.split('/')[-1][:-5].split(',')

    tab = Table.read(lc)
    print(tab)

    res = {}
    res['simbad_name']   = sp[0]
    res['readable_name'] = source_names_readable[sp[0]]
    res['filter']        = sp[1].split('_')[-1]
    res['N']             = len(tab)
    res['SRCEXP_TOT']    = np.sum(tab['SRCEXP'])
    t_diff               = np.diff(tab['MET'])
    res['t_diff_mean']   = np.mean(t_diff)
    res['t_diff_std']    = np.std(t_diff)
    res['t_diff_n_sigma'] = res['t_diff_mean'] / res['t_diff_std']
    res['MAG_MEAN']       = np.mean(tab['MAG'])
    res['COI_SRC_RATE_MEAN'] = np.mean(tab['COI_SRC_RATE'])
    print(res)
    return res


all_res = []
for lc in uvot_lightcurves:
    try:
        res = analyse_uvot_lc(lc)
        all_res.append(res)
    except:
        print(f'Could not process {lc}')
df_res = pd.DataFrame(all_res)
print(df_res)
df_res.to_csv('tables/uvot_lc_info.csv')
