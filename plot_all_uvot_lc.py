from glob import glob
import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table
from uvot import filter_colors
from astropy.time import Time
from astropy.stats import sigma_clip

uvotsource_files = glob('download_scripts/*/*uvotsource*.fits')

for f in uvotsource_files:
    tab = Table.read(f)
    local_name = f.split('/')[-2]
    fn = f.split('/')[-1][:-5]

    tab['MJD'] = 51910 + (tab['MET']/86400)


    """
    plt.figure(figsize=(10,5))
    plt.title(f)
    for f in np.unique(tab['FILTER']):
        sub = tab[tab['FILTER'] == f]
        plt.errorbar(range(len(sub)), sub['COI_SRC_RATE'], yerr=sub['COI_SRC_RATE_ERR'],
        marker='.', markersize=2.0, lw=1.0, capsize=1.0, label=f'{f}', color=filter_colors[f])
    plt.legend()
    plt.savefig(f'figures/uvotsource_plot/{local_name},{fn}.png', bbox_inches='tight')
    plt.savefig(f'figures/uvotsource_plot/{local_name},{fn}.pdf', bbox_inches='tight')

    # Plot MJD
    plt.figure(figsize=(10,5))

    plt.title(f)
    for f in np.unique(tab['FILTER']):
        sub = tab[tab['FILTER'] == f]
        plt.errorbar(sub['MJD'], sub['COI_SRC_RATE'], yerr=sub['COI_SRC_RATE_ERR'],
        marker='.', markersize=2.0, lw=1.0, capsize=1.0, label=f'{f}', color=filter_colors[f],
        ls='none')
        
    plt.legend()
    plt.savefig(f'figures/uvotsource_plot/{local_name},{fn}_MJD.png', bbox_inches='tight')
    plt.savefig(f'figures/uvotsource_plot/{local_name},{fn}_MJD.pdf', bbox_inches='tight')

    """
    # PLOT MAG
    plt.figure(figsize=(10,5))
    plt.title(f)
    for f in np.unique(tab['FILTER']):
        sub = tab[tab['FILTER'] == f]
        sub = sub[sub['MAG']!=99]
        sub = sub[sub['MAG_ERR'] < 5]
        ma = sigma_clip(sub['MAG'], sigma=5, maxiters=1)
        try:
            sub = sub[~ma.mask]
        except:
            pass
        ma = sigma_clip(sub['MAG_ERR'], sigma=5, maxiters=1)
        try:
            sub = sub[~ma.mask]
        except:
            pass

        plt.errorbar(range(len(sub)), sub['MAG'], yerr=sub['MAG_ERR'],
        marker='.', markersize=2.0, lw=1.0, capsize=1.0, label=f'{f}', color=filter_colors[f])
    plt.legend()
    plt.savefig(f'figures/uvotsource_plot/{local_name},{fn}_MAG.png', bbox_inches='tight')
    plt.savefig(f'figures/uvotsource_plot/{local_name},{fn}_MAG.pdf', bbox_inches='tight')

