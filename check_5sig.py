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
    local_name    = source_names_dict[simbad_name]

    print(f'uvot_filter = {uvot_filter}')
    print(f'simbad_name = {simbad_name}')
    print(f'readable_name = {readable_name}')
    print(f'local_name = {local_name}')

    # Setup Paths
    plot_path = Path(f'/mnt/d/anticorr_data/lightcurves/correlation_output/{simbad_name}/plots')
    table_path = Path(f'/mnt/d/anticorr_data/lightcurves/correlation_output/{simbad_name}/tables')
    #plot_path.mkdir(parents=True, exist_ok=True)
    #table_path.mkdir(parents=True, exist_ok=True)
    
    outfile = f'{simbad_name},{xrt_curve},{uvot_filter},{include_bad},{include_UL}'
    #out_table_prop = table_path/f'{outfile},table_prop.csv'
    #out_table_mc   = table_path/f'{outfile},table_corr_mc.csv'
    #out_plot_corr_png  = plot_path/f'{outfile},corr.png'
    #out_plot_corr_pdf  = plot_path/f'{outfile},corr.pdf'
   
    
    ###############
    # Get subsets # 
    ###############

    tab = Table.read(fits_path)
    print(tab)
    print(tab['OBSID','COI_SRC_RATE','COI_SRC_RATE_ERR', 'Rate','Ratepos','Rateneg'])
    
    tables = calc_subsets(tab)
    tab_5_sig        = tables['tab_5_sig']
    tab_UL           = tables['tab_UL']
    tab_no_UL        = tables['tab_no_UL']
    tab_BAD          = tables['tab_BAD']
    tab_no_BAD       = tables['tab_no_BAD']
    tab_UL_no_bad    = tables['tab_UL_no_bad']
    tab_no_UL_no_bad = tables['tab_no_UL_no_bad']
    
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
    print(f'local_name    = {local_name}')

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
    #print(df_tab_prop)
    #print(f'Saving to: {out_table_prop}')
    #df_tab_prop.to_csv(out_table_prop, index=False)
    


    print('----------------------')
    print('Excluded Observations:')
    print('----------------------')
    excluded_obs = {}
    excluded_obs['tab_5_sig']         = get_exluded_obs(tab, tab_5_sig)
    #excluded_obs['tab_UL']           = get_exluded_obs(tab, tab_UL)
    #excluded_obs['tab_no_UL']        = get_exluded_obs(tab, tab_no_UL)
    #excluded_obs['tab_BAD']          = get_exluded_obs(tab, tab_BAD)
    #excluded_obs['tab_no_BAD']       = get_exluded_obs(tab, tab_no_BAD)
    #excluded_obs['tab_UL_no_bad']    = get_exluded_obs(tab, tab_UL_no_bad)
    #excluded_obs['tab_no_UL_no_bad'] = get_exluded_obs(tab, tab_no_UL_no_bad)

    lines_ds9 = []
    for k, v in excluded_obs.items():
        print(f'{k} : ')
        print(v)
        if len(v) > 0:
            for obsid in v:

                img_files = glob(f'download_scripts/{local_name}/{obsid}/*_sk.img.gz')
                reg_files = glob(f'download_scripts/{local_name}/*.reg')
    
    
                if len(img_files)==0:
                   continue 
    
                file_img        = img_files[0] 
                file_src_region = reg_files[0]
                file_bkg_region = reg_files[1]
    
                print('Found 5sig')
                crap = tab[tab['OBSID'] == v]['OBSID','COI_SRC_RATE','COI_SRC_RATE_ERR', 'Rate','Ratepos','Rateneg']
                print(crap)



                xrtr = crap[xrt_rate][0]
                uvotr = crap[uvot_rate][0]

                xrt_rate_mean  = np.mean(tab[xrt_rate])
                uvot_rate_mean = np.mean(tab[uvot_rate])

                xrt_rate_std  = np.std(tab[xrt_rate])
                uvot_rate_std = np.std(tab[uvot_rate])

                xrt_g_5sig = xrt_rate_mean+5*xrt_rate_std
                xrt_l_5sig = xrt_rate_mean-5*xrt_rate_std

                uvot_g_5sig = uvot_rate_mean+5*uvot_rate_std
                uvot_l_5sig = uvot_rate_mean-5*uvot_rate_std

                xrt_dev = (xrtr - xrt_rate_mean) / xrt_rate_std
                uvot_dev = (uvotr - uvot_rate_mean) / uvot_rate_std

                xrt_label = ''
                uvot_label = ''
                if xrtr > xrt_g_5sig:
                    xrt_label ='[xrt hi]'
                if xrtr < xrt_l_5sig:
                    xrt_label = '[xrt_lo]'
                if uvotr > uvot_g_5sig:
                    uvot_label ='[uvot hi]'
                if uvotr < uvot_l_5sig:
                    uvot_label = '[uvot lo]'



               
                lines =[f"echo Source Name = {readable_name}\n",
                        f"echo UVOT filter = {uvot_filter}\n",
                        f"echo obsid = {obsid}\n",
                        f"echo uvot_rate={uvotr:.4f} [{uvot_dev:.4f} sig] mu={uvot_rate_mean:.4f} std={uvot_rate_std:.4f}  +5std={uvot_g_5sig:.4f}    -5std={uvot_l_5sig:.4f} {uvot_label}\n",
                        f"echo xrt_rate ={xrtr:.4f}  [{xrt_dev:.4f} sig]  mu={xrt_rate_mean:.4f}  std={xrt_rate_std:.4f}   +5std={xrt_g_5sig:.4f}     -5std={xrt_l_5sig:.4f} {xrt_label}\n"]

                line_ds9 = f"ds9 -tile {file_img} -region {file_src_region} -region {file_bkg_region} -scale log -zoom to fit -cmap b\n"
                print(line_ds9)

                with open('ds9_5sig.sh', 'a') as f:
                    f.writelines(lines)
                    f.write(line_ds9)

        print('='*50)
    return res



if __name__ == "__main__":
    curve_nosys_files = glob(f'lightcurves/joined/*curve_nosys*.fits')
    hardrat_files     = glob(f'lightcurves/joined/*hardrat*.fits')
    
    print(f'N_hardrat_files={len(hardrat_files)} N_curve_nosys_files={len(curve_nosys_files)}')
    print('Press any key to start, Ctrl+C to quit')
    for fits_path in curve_nosys_files:
        try:
            correlate(fits_path, include_bad=True, include_UL=True)
        except Exception as e:
            line = f"#{fits_path} : Error: {e}\n"
            with open('ds9_5sig.sh', 'a') as f:
                f.write(f'{line}')


        print('#'*50)
        print('#'*50)

    for fits_path in hardrat_files:
        correlate(fits_path, include_bad=True, include_UL=False)
        correlate(fits_path, include_bad=False, include_UL=False)
        print('#'*50)
        print('#'*50)

