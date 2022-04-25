import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table
from astropy.time import Time

def calc_uvot_flags(table):
    table['FLAG_AB_MAG_99']      = table['AB_MAG'] == 99
    table['FLAG_UPPER_LIM']      = table['NSIGMA'] < table['MAG_LIM_SIG'] 
    table['FLAG_AB_MAG_ERR>2']   = table['AB_MAG_ERR'] > 2
    table['FLAG_AB_MAG_>10_<30'] = np.logical_or((table['AB_MAG'] < 10), (table['AB_MAG'] > 30))
    
    print('UVOT flag summary:')
    print(f'FLAG_AB_MAG_99      = {np.sum(table["FLAG_AB_MAG_99"])} / {len(table)} ({np.sum(table["FLAG_AB_MAG_99"]) / len(table) * 100 :.2f}%)')
    print(f'FLAG_UPPER_LIM      = {np.sum(table["FLAG_UPPER_LIM"])} / {len(table)} ({np.sum(table["FLAG_UPPER_LIM"]) / len(table) * 100 :.2f}%)')
    print(f'FLAG_AB_MAG_ERR>2   = {np.sum(table["FLAG_AB_MAG_ERR>2"])} / {len(table)} ({np.sum(table["FLAG_AB_MAG_ERR>2"]) / len(table) * 100 :.2f}%)')
    print(f'FLAG_AB_MAG_>10_<30 = {np.sum(table["FLAG_AB_MAG_>10_<30"])} / {len(table)} ({np.sum(table["FLAG_AB_MAG_>10_<30"]) / len(table) * 100 :.2f}%)')
    print('==================')
    return table

def read_uvotsource(path, filter_flags=False):
    print('Reading uvotsource...')
    print(f'Reading file {path}')
    tab = Table.read(path)
    n_unique_obs = len(np.unique(tab['OBSID']))
    print(f'tab len={len(tab)} unique_obs={n_unique_obs}')
    
    tab.sort('MET')
    MJDREFI = 51910
    tab['MJD'] = MJDREFI  + tab['MET'] / 86400.0
    tab['YEAR'] = Time(np.array(tab['MJD']), format='mjd').decimalyear
    tab['MJD_0'] = tab['MJD'] - tab['MJD'].min()
    
    tab = calc_uvot_flags(tab)
    tab = tab[~tab['FLAG_AB_MAG_99']]
    tab = tab[~tab['FLAG_UPPER_LIM']]
    tab = tab[~tab['FLAG_AB_MAG_ERR>2']]
    return tab




# Plotting Functions

def plot_uvotsource_lc(path, ax=None):
    tab = read_uvotsource(path)
    if ax is None:
        fig, ax = plt.subplots(figsize=(20,5))
    ax.set_title(path)
    for f in np.unique(tab['FILTER']):
        sub = tab[tab['FILTER'] == f]
        ax.errorbar(sub['MJD'], sub['MAG'], sub['MAG_ERR'], ls='none', lw=1.0, capsize=1.0, label=f)
    ax.legend()


filters = ['B', 'U', 'V', 'UVM2', 'UVW1', 'UVW2', 'WHITE']
filter_colors = {'B'    : 'steelblue',
                 'U'    : 'indigo',
                 'V'    : 'green',
                 'UVM2' : 'magenta',
                 'UVW1' : 'cyan',
                 'UVW2' : 'orange',
                 'WHITE': 'gray'}

filter_markers = {'B'    : '.',
                  'U'    : 'v',
                  'V'    : '^',
                  'UVM2' : 's',
                  'UVW1' : 'x',
                  'UVW2' : '+',
                  'WHITE': '*'}

