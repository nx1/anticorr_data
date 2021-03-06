from os.path import exists
import numpy as np
import pandas as pd
from astroquery.heasarc import Heasarc
from astropy.table import vstack
from source_names_dict import source_names_dict

source_names = list(source_names_dict.keys())


h = Heasarc()

all_summary = []
all_tabs = []

for i, s in enumerate(source_names):
    summary = {}
    print(f'Querying {s} ({i}/{len(source_names)})')
    s_sp = s.replace('_',' ') # Heasarc does not like underscores :(
    tab = h.query_object(s_sp, mission='XMMMASTER', resultmax=3000)
    tab['SEARCH_NAME'] = s
    print(tab)
    summary['source_name'] = s
    summary['n_obs'] = len(tab)
    print(summary)
    all_summary.append(summary)
    all_tabs.append(tab)
    
df_all_summary = pd.DataFrame(all_summary).sort_values('n_obs', ascending=False)
tab_master = vstack(all_tabs)
print(df_all_summary)

print('Looping over obsids to create shell script...')
all_lines = []
for row in tab_master:
    source_name = row['SEARCH_NAME']
    obsid       = row['OBSID']
    filepath = f'xmm/{source_name}/{obsid}.tar' 
    line = f'curl -o {filepath} "http://nxsa.esac.esa.int/nxsa-sl/servlet/data-action-aio?obsno={obsid}" --create-dirs'
    if exists(filepath):
        line = '#'+ line
    all_lines.append(line)

download_sh = 'download_xmm.sh'

with open(download_sh, 'w+') as f:
    for l in all_lines:
        f.write(f'{l}\n')

print(f'File written to {download_sh}')

savepath = 'tables/xmmmaster_n_obs.csv'
savepath_master = 'tables/xmmmaster.csv'
print(f'saving to {savepath}')
print(f'saving to {savepath_master}')
df_all_summary.to_csv(savepath, index=False)
tab_master.write(savepath_master, overwrite=True)
n_obs_tot = df_all_summary["n_obs"].sum()
print(f'Total obs={n_obs_tot} \t estimated size = {0.025*n_obs_tot} gb')
