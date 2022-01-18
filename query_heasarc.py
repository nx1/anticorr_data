from source_names import source_names
import numpy as np
import pandas as pd
from astroquery.heasarc import Heasarc

h = Heasarc()

all_summary = []

for i, s in enumerate(source_names):
    summary = {}
    print(f'Querying {s} ({i}/{len(source_names)})')
    s_sp = s.replace('_',' ') # Heasarc does not like underscores :(
    tab = h.query_object(s_sp, mission='SWIFTMASTR', resultmax=3000)
    tab['SEARCH_NAME'] = s
    print(tab)
    summary['source_name'] = s
    summary['n_obs'] = len(tab)
    summary['n_obs_uvot'] = np.count_nonzero(tab['UVOT_EXPOSURE'])
    summary['n_obs_xrt']  = np.count_nonzero(tab['XRT_EXPOSURE'])
    summary['total_uvot_exp'] = tab['UVOT_EXPOSURE'].sum()
    summary['total_xrt_exp']  = tab['XRT_EXPOSURE'].sum()
    print(summary)
    all_summary.append(summary)
    
df_all_summary = pd.DataFrame(all_summary).sort_values('n_obs', ascending=False)
print(df_all_summary)
n_obs_tot = df_all_summary["n_obs"].sum()
print(f'Total obs={n_obs_tot} \t estimated size = {0.025*n_obs_tot} gb')
