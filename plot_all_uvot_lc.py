from glob import glob
import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table


maghist_files = glob('download_scripts/*/*maghist_all.fits')
for f in maghist_files:
    tab = Table.read(f)
    
    tab = tab[tab['AB_MAG'] < 50]
    tab = tab[tab['AB_MAG_ERR'] < 100]
    
    plt.figure(figsize=(20,5))
    plt.title(f)
    for f in np.unique(tab['FILTER']):
        
        sub = tab[tab['FILTER'] == f]
        plt.errorbar(sub['MET'], sub['AB_MAG'], yerr=sub['AB_MAG_ERR'], marker='.', markersize=2.0, ls='none', lw=1.0, capsize=1.0, label=f'Filter: {f}')
    plt.legend()
plt.show()
