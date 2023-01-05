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
    all_tabs.append(tab)

tab_all = vstack(all_tabs)
tab_all.write('tables/swiftmaster_all_tables.csv', overwrite=True)
tab_all.write('tables/swiftmaster_all_tables.fits', overwrite=True)


df_all_summary = pd.DataFrame(all_summary).sort_values('n_obs', ascending=False)
df_all_summary.to_csv('tables/swiftmaster_summary.csv')
df_all_summary.to_latex('tables/swiftmaster_summary.tex', index=False)
print(df_all_summary)
n_obs_tot = df_all_summary["n_obs"].sum()
