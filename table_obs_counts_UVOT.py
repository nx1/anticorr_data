import numpy as np
from glob import glob
import pandas as pd
import matplotlib.pyplot as plt
from astropy.table import Table

from uvot import filter_colors
from source_names_dict import source_names_dict, source_names_readable, source_distances_mpc, get_simbad_name_glob
pd.set_option('display.max_columns', None)

rows  = []  # For storing obs counts (latex)
rows4 = []  # For storing obs counts (csv)
rows2 = []  # For storing fluxes (latex)
rows3 = []  # For storing fluxes (numerical)
rows5 = []  # For storing obs counts and fluxes

for simbad_name, readable_name in source_names_readable.items():
    print(f'Doing {simbad_name} {readable_name}')
    simbad_name_glob = get_simbad_name_glob(simbad_name)
    files = glob(f'lightcurves/uvot/*{simbad_name_glob}*')
    
    row   = {'simbad_name': simbad_name, 'readable_name':readable_name}
    row2  = {'simbad_name': simbad_name, 'readable_name':readable_name}
    row3  = {'simbad_name': simbad_name, 'readable_name':readable_name}
    row4  = {'simbad_name': simbad_name, 'readable_name':readable_name}
    row5  = {'simbad_name': simbad_name, 'readable_name':readable_name}


   
    for f in files:
        uvot_filter = f.split('/')[-1][:-5].split(',')[1].split('_')[1]
        tab = Table.read(f)

        n_obs = len(np.unique(tab['OBSID']))
        n_det = np.sum((tab['NSIGMA'] > 3))
        
        rate_mu  = np.mean(tab['COI_SRC_RATE'])
        rate_std = np.std(tab['COI_SRC_RATE'])
        
        row[f'{uvot_filter}']      = f'{n_obs} ({n_det})'
        row2[f'{uvot_filter}']     = f'{rate_mu:.2f} $\pm$ {rate_std:.2f}'
        row3[f'{uvot_filter}_mu']  = rate_mu
        row3[f'{uvot_filter}_std'] = rate_std
        
        row4[f'{uvot_filter}_n_obs'] = n_obs
        row4[f'{uvot_filter}_n_det'] = n_det

        row5[f'{uvot_filter}_n_obs']     = n_obs
        row5[f'{uvot_filter}_n_det_3_sig'] = n_det
        row5[f'{uvot_filter}_rate_mean'] = rate_mu
        row5[f'{uvot_filter}_rate_std']  = rate_std







    rows.append(row)
    rows2.append(row2)
    rows3.append(row3)
    rows4.append(row4)
    rows5.append(row5)


df_uvot_counts = pd.DataFrame(rows)
df_uvot_counts = df_uvot_counts.set_index('simbad_name').loc[list(source_distances_mpc.keys())]
df_uvot_counts = df_uvot_counts.fillna(0).reset_index()

print('df_uvot_counts:')
print(df_uvot_counts)

df_uvot_counts_csv = pd.DataFrame(rows4)
df_uvot_counts_csv = df_uvot_counts.set_index('simbad_name').loc[list(source_distances_mpc.keys())]
df_uvot_counts_csv = df_uvot_counts.fillna(0).reset_index()

print('df_uvot_counts_csv:')
print(df_uvot_counts_csv)


df_uvot_rates = pd.DataFrame(rows2)
df_uvot_rates = df_uvot_rates.set_index('simbad_name').loc[list(source_distances_mpc.keys())]
df_uvot_rates = df_uvot_rates.fillna(0).reset_index()
print('df_uvot_rates')
print(df_uvot_rates)

df_uvot_rates2 = pd.DataFrame(rows3)
df_uvot_rates2 = df_uvot_rates2.set_index('simbad_name').loc[list(source_distances_mpc.keys())]
print('df_uvot_rates2:')
print(df_uvot_rates2)

df_uvot = pd.DataFrame(rows5)
df_uvot = df_uvot.set_index('simbad_name').loc[list(source_distances_mpc.keys())]
print('df_uvot:')
print(df_uvot)



outfile_uvot_n_obs = 'tables/uvot_n_obs.tex'
outfile_uvot_flux  = 'tables/UVOT_FLUX.tex'

outfile_uvot_n_obs_csv = 'tables/uvot_n_obs.csv'
outfile_uvot_flux_csv  = 'tables/UVOT_FLUX.csv'

outfile_uvot_csv = 'tables/UVOT_obs_rates.csv'


df_save = df_uvot_counts[['readable_name', 'U', 'B', 'V', 'UVM2', 'UVW1', 'UVW2', 'WHITE']]
print(f'Saving to: {outfile_uvot_n_obs}')
df_save.to_latex(outfile_uvot_n_obs, index=False, escape=False)

#print(f'Saving to: {outfile_uvot_n_obs_csv}')
#df_save.to_csv(outfile_uvot_n_obs_csv, index=False)

print(f'Saving to: {outfile_uvot_flux}')
print(f'Saving to: {outfile_uvot_flux_csv}')
df_save.to_latex(outfile_uvot_flux, index=False, escape=False)
df_save.to_csv(outfile_uvot_flux_csv, index=False)


print(f'Saving to: {outfile_uvot_csv}')
df_uvot.to_csv(outfile_uvot_csv, index=False)
