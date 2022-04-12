from glob import glob

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from astropy.table import Table

from uvot import read_uvotsource, calc_uvot_flags, plot_uvotsource_lc

def get_gtis(t):
    diff = np.diff(t)
    mu   = np.mean(diff)
    #lo  = mu - np.std(diff)
    hi   = mu + np.std(diff)

    max_diff = hi
    
    if len(diff) > 10:
        gap_indexs = []
        for i, val in enumerate(diff):
            # print(f'i={i} t[i]={t[i]:.2f} y[i]={y[i]:.2f} y_err={y_err[i]:.2f}')
            if val > max_diff:
                print(f'i={i} t[i]={t[i]:.2f} y[i]={y[i]:.2f} y_err={y_err[i]:.2f} max diff exceeded! val>max_diff ({val:.2f}>{hi:.2f})')
                gap_indexs.append([i, i+1])

        # Turn the bad intervals into good intervals                        
        gti_indexs = []
        first = [0, gap_indexs[0][0]] # Get the gti for the data at the start
        gti_indexs.append(first)                                                  
                                                                        
        for i in range(len(gap_indexs)-1):
            #print([0, gti_indexs[i][0]])
            term = [gap_indexs[i][1], gap_indexs[i+1][0]]
            gti_indexs.append(term)
                                                                        
        last = [gap_indexs[-1][1], len(tab)-1] # get the gtis for the data at the end
        gti_indexs.append(last)

        gtis = [[int(t[s]), int(t[e])+1] for s, e in gti_indexs]
        print(gti_indexs)
        print(gtis)
        return gti_indexs, gtis
    else:
        return [], []


def calc_von_neumann_stat(y):
    """
    Ann. Math. Statist. 12(4): 367-395 (December, 1941).
    dio: 10.1214/aoms/1177731677
    """
    print('Calculating Von-Neumann Statistic...')
    if len(y) < 10:
        return 99

    s2 = np.var(y)
    n = len(y)
    print(f'{n}={n} var={s2}')
    sumtot = 0
    for i in range(len(y)-1):
        term = (y[i+1] - y[i])**2
        sumtot += term
        print(f'i={i} y[i]={y[i]:.4f} y[i+1]={y[i+1]:.4f} term={term:.2f} sumtot={sumtot:.2f}')
    eta = ((1 / (n-1)) * sumtot) / s2
    print(f'eta = {eta}')
    return eta

def calc_skewness(y):
    print('Calculating skewness...')
    if len(y) < 10:
        return 99

    s3 = np.std(y)**3
    n = len(y)
    mean = np.mean(y)

    print(f'{n}={n} s3={s3}')
    sumtot = 0
    for i in range(len(y)-1):
        term = (y[i] - mean)**3
        sumtot += term
        print(f'i={i} y[i]={y[i]:.4f} mean={mean:.4f} term={term:.2f} sumtot={sumtot:.2f}')
    gamma = ((1 / (n)) * sumtot) / s3
    print(f'gamma={gamma}')
    return gamma

def calc_sigma_xs(y, y_err):
    """Calculate the excess variance.
    See equation (8) and (9)
    https://ui.adsabs.harvard.edu/abs/2003MNRAS.345.1271V/abstract
    """
    if len(y) < 10:
        return 99
    N = len(y)
    sigma_err_2 = (1/N) * np.sum(y_err**2)
    S2 = np.var(y, ddof=1)    # See equation (6)
    sigma_xs = S2 - sigma_err_2
    return sigma_xs

def calc_F_var(y, y_err):
    """Calculate the fractional variance"""
    if len(y) < 10:
        return 99
    N = len(y)
    sigma_err_2 = (1/N) * np.sum(y_err**2)
    S2 = np.var(y, ddof=1)    # See equation (6)
    F_var = np.sqrt((S2 - sigma_err_2) / np.mean(y)**2)
    return F_var

if __name__ == "__main__":
    print('Lightcurve plotter')

    lc_files = glob('lightcurves/*.fits')
    all_dicts = []

    for path in lc_files:
        print(path)
        d = {}
        fn = path.split('/')[-1][:-5] # Filename without extension
        simbad_name, lc_name = fn.split(',')

        fig, ax = plt.subplots(2,1, figsize=(10,6))
        ax[0].set_title(simbad_name)

        if 'UVOT' in lc_name:
            tab = read_uvotsource(path)
            t     = tab['MJD']
            y     = tab['MAG']
            y_err = tab['MAG_ERR']

        if 'XRT' in lc_name:
            tab = Table.read(path)
            t = tab['MJD']
            y = tab['RATE']
            y_err = tab['RATE_ERR']

        ax[0].errorbar(t, y, y_err, lw=1.0, capsize=1.0, ls='none', label=lc_name)
        ax[0].legend()

        gti_indexs, gtis = get_gtis(t)

        print(gti_indexs)
        print(gtis)

        if len(gtis) > 0:
            # Plot GTIs & extract lightcurve segements
            for gti in gtis:
                s, e = gti

                sub = tab[(tab['MJD'] > s) & (tab['MJD'] < e)]
                out_fn = f'lightcurves/segments/{simbad_name},{lc_name},{s},{e}.fits'
                print(f'writing to {out_fn}')
                sub.write(out_fn, format='fits', overwrite=True)
                ax[0].axvspan(s, e, color='green', alpha=0.5)

            # Plot diff
            diff = np.diff(tab['MJD'])
            mu = np.mean(tab['MJD'])
            hi = mu + np.std(tab['MJD'])
            ax[1].plot(diff)
            ax[1].axhline(mu, ls='dotted', color='green')
            ax[1].axhspan(0, hi , alpha=0.5, color='cyan', ec='black')



        d['path']        = path
        d['simbad_name'] = simbad_name
        d['lc_name']     = lc_name
        d['ndata']       = len(tab)
        d['mean']        = np.mean(y)
        d['std']         = np.std(y)
        d['var']         = np.var(y)
        d['sigma_xs']    = calc_sigma_xs(y, y_err)
        d['F_var']       = calc_F_var(y, y_err)
        d['von_n']       = calc_von_neumann_stat(y)
        d['skewness']    = calc_skewness(y)
        print(d)
        all_dicts.append(d)
        print(path)
        plt.savefig(f'figures/lc_gtis/{simbad_name}_{lc_name}.png')
        plt.savefig(f'figures/lc_gtis/{simbad_name}_{lc_name}.pdf')




    df = pd.DataFrame(all_dicts)
    print(df)
    savepath_df = 'lightcurves/statistics.csv'
    print(f'saving dataframe to: {savepath_df}')
    df.to_csv(savepath_df)

