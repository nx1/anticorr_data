import numpy as np
bs_counts_XRT.pytable_obs_counts_XRT.py
from glob import glob
import pandas as pd
import matplotlib.pyplot as plt
from astropy.table import Table

from uvot import filter_colors
from source_names_dict import source_names_dict, source_names_readable, source_distances_mpc, get_simbad_name_glob
pd.set_option('display.max_columns', None)

rows = []
rows2 = []
for simbad_name, readable_name in source_names_readable.items():
    simbad_name_glob = get_simbad_name_glob(simbad_name)
    files = glob(f'lightcurves/xrt/*{simbad_name_glob}*')
    
    for f in files:
        if 'hardrat' in f:
            df_hardrat = pd.read_csv(f,dtype={'obsID':'str'})
            df_hard = df_hardrat[df_hardrat['BAND'] == 'HARD']
            df_soft = df_hardrat[df_hardrat['BAND'] == 'SOFT']
            df_hr   = df_hardrat[df_hardrat['BAND'] == 'HR']
        if 'nosys' in f:
            df = pd.read_csv(f,dtype={'obsID':'str'})
            
    n_obs = len(df)
    n_ul   = df['UL'].sum()
    n_bad  = df['BAD'].sum()
    n_good = len(df[df['BAD'] == False])
    
    cr_mean = df[df['BAD'] == False]['Rate'].mean()
    cr_std = df[df['BAD'] == False]['Rate'].std()
    cr_soft_mean = df_soft[df_soft['BAD'] == False]['Rate'].mean()
    cr_soft_std  = df_soft[df_soft['BAD'] == False]['Rate'].std()
    cr_hard_mean = df_hard[df_hard['BAD'] == False]['Rate'].mean()
    cr_hard_std  = df_hard[df_hard['BAD'] == False]['Rate'].std()
    cr_hr_mean   = df_hr[df_hr['BAD'] == False]['Rate'].mean()
    cr_hr_std    = df_hr[df_hr['BAD'] == False]['Rate'].std()
    
    cr_full_str = f"{df[df['BAD'] == False]['Rate'].mean():.2f} $\pm$ {df[df['BAD'] == False]['Rate'].std():.2f}"
    cr_soft_str = f"{df_soft[df_soft['BAD'] == False]['Rate'].mean():.2f} $\pm$ {df_soft[df_soft['BAD'] == False]['Rate'].std():.2f}"
    cr_hard_str = f"{df_hard[df_hard['BAD'] == False]['Rate'].mean():.2f} $\pm$ {df_hard[df_hard['BAD'] == False]['Rate'].std():.2f}"
    cr_hr_str   = f"{df_hr[df_hr['BAD'] == False]['Rate'].mean():.2f} $\pm$ {df_hr[df_hr['BAD'] == False]['Rate'].std():.2f}"
    
    row = {'simbad_name':simbad_name, 'readable_name' : readable_name,
           'OBS':n_obs, 'UL' : n_ul, 'BAD': n_bad, 'GOOD': n_good,
           'FULL_mu' : cr_mean, 'FULL_std' : cr_std,
           'SOFT_mu' : cr_soft_mean, 'SOFT_std': cr_soft_std,
           'HARD_mu' : cr_hard_mean, 'HARD_std': cr_hard_std,
           'HR_mu' : cr_hr_mean, 'HR_std': cr_hr_std}
    
    row2 = {'simbad_name':simbad_name, 'readable_name' : readable_name,
            'OBS':n_obs, 'UL' : n_ul, 'BAD': n_bad, 'GOOD': n_good,
            'FULL': cr_full_str,
            'SOFT': cr_soft_str,
            'HARD': cr_hard_str,
            'HR': cr_hr_str,
           }
    
    rows.append(row)
    rows2.append(row2)


df_obs_counts = pd.DataFrame(rows)
df_obs_counts = df_obs_counts.set_index('simbad_name').loc[list(source_distances_mpc.keys())[::-1]].reset_index()
print('df_obs_counts:')
print(df_obs_counts)

df_obs_counts_latex = pd.DataFrame(rows2)
df_obs_counts_latex = df_obs_counts_latex.set_index('simbad_name').loc[list(source_distances_mpc.keys())[::-1]]
df_obs_counts_latex = df_obs_counts_latex.reset_index()[['readable_name','OBS','UL','BAD','GOOD', 'FULL', 'SOFT', 'HARD', 'HR']]

print('df_obs_counts_latex:')
print(df_obs_counts_latex)

outfile_obs_rates = 'tables/XRT_obs_rates.tex'
outfile_obs_rates_csv = 'tables/XRT_obs_rates.csv'

print(f'Saving to: {outfile_obs_rates}')
print(f'Saving to: {outfile_obs_rates_csv}')

df_obs_counts_latex.to_latex(outfile_obs_rates, index=False, escape=False)
df_obs_counts.to_csv(outfile_obs_rates_csv, index=False)


df2 = df_obs_counts.set_index('readable_name')
df_rates_dim = df2[df2['FULL_mu'] < 0.25][['FULL_mu', 'SOFT_mu', 'HARD_mu']]
df_rates_err_dim = df2.loc[df_rates_dim.index][['FULL_std', 'SOFT_std', 'HARD_std']]
df_rates_dim.columns = ['FULL','SOFT','HARD']
df_rates_err_dim.columns = ['FULL','SOFT','HARD']

print(df2)
