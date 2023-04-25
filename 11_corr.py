import warnings
from glob import glob
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from scipy.optimize import curve_fit
import pandas as pd
from tqdm import tqdm
from astropy.time import Time
from astropy.table import Table
from astropy.units import UnitsWarning

from source_names_dict import source_names_dict, source_names_w_counterparts, source_names_readable

warnings.filterwarnings('ignore', category=UnitsWarning, append=True)

def line(x, m, c):
    return m*x+c

def df_properties(tab, tab_name):
    prop = {}
    prop['name']   = tab_name
    prop['length'] = len(tab)
    prop['N_obs']  = len(np.unique(tab["OBSID"]))
    prop['N_bad']  = len(tab[tab['BAD'] == True])
    prop['N_good'] = len(tab[tab['BAD'] == False])
    prop['N_UL']   = len(tab[tab['UL'] == True])
    return prop
    
def get_exluded_obs(tab_big, tab_small):
    obs1 = np.unique(tab_big['OBSID'])
    obs2 = np.unique(tab_small['OBSID'])
    obs_excluded = np.setdiff1d(obs1,obs2)
    obs_excluded = list(obs_excluded)
    return obs_excluded

def calc_subsets(tab):
    uvot_rate     = 'COI_SRC_RATE'
    uvot_rate_err = 'COI_SRC_RATE_ERR'
    xrt_rate      = 'Rate'
    xrt_rate_err  = 'Ratepos'
    
    
    tables = {}
    
    # Add idx column for original position
    tab['idx'] = range(len(tab))
    
    
    # Filter out 5 sigma outliers
    xrt_rate_mean  = np.mean(tab[xrt_rate])
    uvot_rate_mean = np.mean(tab[uvot_rate])

    xrt_rate_std  = np.std(tab[xrt_rate])
    uvot_rate_std = np.std(tab[uvot_rate])

    tables['tab_5_sig'] = tab[(tab[xrt_rate] < xrt_rate_mean + 5 * xrt_rate_std)
                            & (tab[xrt_rate] > xrt_rate_mean - 5 * xrt_rate_std)
                            & (tab[uvot_rate] < uvot_rate_mean + 5 * uvot_rate_std)
                            & (tab[uvot_rate] > uvot_rate_mean - 5 * uvot_rate_std)]

    # Get UL and BAD subsets
    tab_5_sig = tables['tab_5_sig']
    tables['tab_UL']     = tab_5_sig[tab_5_sig['UL'] == True]
    tables['tab_no_UL']  = tab_5_sig[tab_5_sig['UL'] == False]

    tables['tab_BAD']    = tab_5_sig[tab_5_sig['BAD'] == True]
    tables['tab_no_BAD'] = tab_5_sig[tab_5_sig['BAD'] == False]

    tables['tab_UL_no_bad'] = tab_5_sig[(tab_5_sig['BAD'] == False) & (tab_5_sig['UL'] == True)]
    tables['tab_no_UL_no_bad'] = tab_5_sig[(tab_5_sig['BAD'] == False) & (tab_5_sig['UL'] == False)]
    return tables
    

def correlate(fits_path, include_bad, include_UL):
    ####################
    # SETUP SIMULATION # 
    ####################

    res = {} # Dictionary for storing results

    # IF YOU CHANGE THIS, CHANGE THEM IN CALC_SUBSETS TOO
    uvot_rate     = 'COI_SRC_RATE'
    uvot_rate_err = 'COI_SRC_RATE_ERR'
    xrt_rate      = 'Rate'
    xrt_rate_err  = 'Ratepos'

    N_mc = 10000
    
    print('correlate()')
    print('----------')
    print('Input:')
    print(f'fits_path   = {fits_path}')
    print(f'include_bad = {include_bad}')
    print(f'include_UL  = {include_UL}')
    print(f'N_mc        = {N_mc}')
    print('')

    if 'curve_nosys' in fits_path:
        xrt_curve = 'FULL'
        xrt_rate_err = 'Ratepos'
    elif 'hardrat' in fits_path:
        xrt_curve = fits_path.split('/')[-1].split(',')[-1][:-5]
        xrt_rate_err = 'Error'

    print('Using XRT curve:')
    print(f'xrt_curve = {xrt_curve}')
    print('')

    print('Using Rates:')
    print(f'uvot_rate     = {uvot_rate}')
    print(f'uvot_rate_err = {uvot_rate_err}')
    print(f'xrt_rate      = {xrt_rate}')
    print(f'xrt_rate_err  = {xrt_rate_err}')
    print('')

    uvot_filter = fits_path.split('/')[-1].split(',')[1]
    simbad_name = fits_path.split('/')[-1].split(',')[0]
    readable_name = source_names_readable[simbad_name]

    print(f'uvot_filter = {uvot_filter}')
    print(f'simbad_name = {simbad_name}')
    print(f'readable_name = {readable_name}')

    # Setup Paths
    plot_path = Path(f'/mnt/d/anticorr_data/lightcurves/correlation_output/{simbad_name}/plots')
    table_path = Path(f'/mnt/d/anticorr_data/lightcurves/correlation_output/{simbad_name}/tables')
    plot_path.mkdir(parents=True, exist_ok=True)
    table_path.mkdir(parents=True, exist_ok=True)
    
    outfile = f'{simbad_name},{xrt_curve},{uvot_filter},{include_bad},{include_UL}'
    out_table_prop = table_path/f'{outfile},table_prop.csv'
    out_table_mc   = table_path/f'{outfile},table_corr_mc.csv'
    out_plot_corr_png  = plot_path/f'{outfile},corr.png'
    out_plot_corr_pdf  = plot_path/f'{outfile},corr.pdf'
    
    if out_table_mc.exists():
        print(f'Monte carlo output table exists!')
        print(f'Skipping fits_path={fits_path} include_bad={include_bad} include_UL={include_UL}')
    
    
    ###############
    # Get subsets # 
    ###############

    tab = Table.read(fits_path)
    print(tab)
    
    tables = calc_subsets(tab)
    tab_5_sig        = tables['tab_5_sig']
    tab_UL           = tables['tab_UL']
    tab_no_UL        = tables['tab_no_UL']
    tab_BAD          = tables['tab_BAD']
    tab_no_BAD       = tables['tab_no_BAD']
    tab_UL_no_bad    = tables['tab_UL_no_bad']
    tab_no_UL_no_bad = tables['tab_no_UL_no_bad']
    


    ###################################
    # Perform lc sampling monte carlo # 
    ###################################

    # Results dictionary
    all_mc_res = []

    for i in tqdm(range(N_mc)):
        mc_res = {}
        if include_bad == True:
            x_samp = np.random.normal(loc=tab_no_UL[xrt_rate], scale=tab_no_UL[xrt_rate_err])
            y_samp = np.random.normal(loc=tab_no_UL[uvot_rate], scale=tab_no_UL[uvot_rate_err])

        elif include_bad == False:
            x_samp = np.random.normal(loc=tab_no_UL_no_bad[xrt_rate], scale=tab_no_UL_no_bad[xrt_rate_err])
            y_samp = np.random.normal(loc=tab_no_UL_no_bad[uvot_rate], scale=tab_no_UL_no_bad[uvot_rate_err])

        # Add in the upper limit samples
        # We treat upper limit values as uniform between 0 and the value
        if include_UL:
            x_samp_UL = np.random.uniform(low=[0]*len(tab_UL), high=tab_UL[xrt_rate])
            y_samp_UL = np.random.uniform(low=[0]*len(tab_UL), high=tab_UL[uvot_rate])

            x_samp = np.concatenate([x_samp_UL, x_samp])
            y_samp = np.concatenate([y_samp_UL, y_samp])

        r, p_val = pearsonr(x_samp,y_samp)
        p_opt, p_cov = curve_fit(line, x_samp, y_samp)
        m, c = p_opt

        mc_res['r'] = r
        mc_res['m'] = m
        mc_res['c'] = c
        all_mc_res.append(mc_res)

    df_mc_res = pd.DataFrame(all_mc_res)
    print(f'Saving to: {out_table_mc}')
    df_mc_res.to_csv(out_table_mc, index=False)

    print('Linear Correlation Test...')
    print('==========================')
    print('--------------------------')

    print('Input Parameters:')
    print('-----------------')
    print(f'include_bad : {include_bad}')
    print(f'include_UL  : {include_UL}')
    print(f'fits_path   : {fits_path}')

    print('---------')
    print('Settings:')
    print('---------')
    print(f'N_mc          = {N_mc}')
    print(f'uvot_rate     = {uvot_rate}')
    print(f'uvot_rate_err = {uvot_rate_err}')
    print(f'xrt_rate      = {xrt_rate}')
    print(f'xrt_rate_err  = {xrt_rate_err}')
    print(f'uvot_filter   = {uvot_filter}')
    print(f'xrt_curve     = {xrt_curve}')
    print(f'simbad_name   = {simbad_name}')
    print(f'readable_name = {readable_name}')

    print('----------------')
    print('Data Properties:')
    print('----------------')
    all_table_properties = [df_properties(tab, "tab"),
                            df_properties(tab_5_sig, "tab_5_sig"),
                            df_properties(tab_UL, "tab_UL"),
                            df_properties(tab_no_UL, "tab_no_UL"),
                            df_properties(tab_BAD, "tab_BAD"),
                            df_properties(tab_no_BAD, "tab_no_BAD"),
                            df_properties(tab_UL_no_bad, "tab_UL_no_bad"),
                            df_properties(tab_no_UL_no_bad, "tab_no_UL_no_bad")]
    df_tab_prop = pd.DataFrame(all_table_properties)
    print(df_tab_prop)
    print(f'Saving to: {out_table_prop}')
    df_tab_prop.to_csv(out_table_prop, index=False)
    


    print('----------------------')
    print('Excluded Observations:')
    print('----------------------')
    excluded_obs = {}
    excluded_obs['tab_5_sig']        = get_exluded_obs(tab, tab_5_sig)
    excluded_obs['tab_UL']           = get_exluded_obs(tab, tab_UL)
    excluded_obs['tab_no_UL']        = get_exluded_obs(tab, tab_no_UL)
    excluded_obs['tab_BAD']          = get_exluded_obs(tab, tab_BAD)
    excluded_obs['tab_no_BAD']       = get_exluded_obs(tab, tab_no_BAD)
    excluded_obs['tab_UL_no_bad']    = get_exluded_obs(tab, tab_UL_no_bad)
    excluded_obs['tab_no_UL_no_bad'] = get_exluded_obs(tab, tab_no_UL_no_bad)
    
    for k, v in excluded_obs.items():
        print(f'{k} : ')
        print(v)
        print('='*50)

    print('-----------------------')
    print('Monte Carlo Fit Results')
    print('-----------------------')

    print(df_mc_res)
    #df_mc_res.to_csv(table_path/f'{outfile},line_mc.csv', index=False)

    # Calculate mean fit values and errors
    res['r_mean'] = df_mc_res['r'].mean()
    res['r_std']  = df_mc_res['r'].std()
    res['m_mean'] = df_mc_res['m'].mean()
    res['m_std']  = df_mc_res['m'].std()
    res['c_mean'] = df_mc_res['c'].mean()
    res['c_std']  = df_mc_res['c'].std()

    print('Best fit params:')
    print(f'r = {res["r_mean"]:.2f} +- {res["r_std"]:.2f}')
    print(f'm = {res["m_mean"]:.2f} +- {res["m_std"]:.2f}')
    print(f'c = {res["c_mean"]:.2f} +- {res["c_std"]:.2f}')
    return res



if __name__ == "__main__":
    curve_nosys_files = glob(f'lightcurves/joined/*curve_nosys*.fits')
    hardrat_files     = glob(f'lightcurves/joined/*hardrat*.fits')
    
    print('correlate.py')
    print('------------')
    print('Test for linear correlation between two bands')
    print(f'N_hardrat_files={len(hardrat_files)} N_curve_nosys_files={len(curve_nosys_files)}')
    print('Press any key to start, Ctrl+C to quit')
    input()
    for fits_path in curve_nosys_files:
        try:
            correlate(fits_path, include_bad=True, include_UL=False)
            input()
            correlate(fits_path, include_bad=False, include_UL=False)
            correlate(fits_path, include_bad=True, include_UL=True)
            correlate(fits_path, include_bad=False, include_UL=True)

        except Exception as e:
            print(f'Error {fits_path} Exception = {e}')

        print('#'*50)
        print('#'*50)

    for fits_path in hardrat_files:
        try:
            correlate(fits_path, include_bad=True, include_UL=False)
            correlate(fits_path, include_bad=False, include_UL=False)
        except Exception as e:
            print(f'Error {fits_path} Exception = {e}')
        print('#'*50)
        print('#'*50)
