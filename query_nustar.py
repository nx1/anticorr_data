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
    tab = h.query_object(s_sp, mission='NUMASTER', resultmax=3000)
    if len(tab) == 0:
        continue
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

savepath = 'tables/numaster_n_obs.csv'
savepath_master = 'tables/nustarmaster.csv'
print(f'saving to {savepath}')
print(f'saving to {savepath_master}')
df_all_summary.to_csv(savepath, index=False)
tab_master.write(savepath_master)
n_obs_tot = df_all_summary["n_obs"].sum()
print(f'Total obs={n_obs_tot} \t estimated size = {0.025*n_obs_tot} gb')
