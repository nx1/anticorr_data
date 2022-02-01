import os
from glob import glob
import pandas as pd

def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size


source_dirs = glob('download_scripts/*/')

print(f'{len(source_dirs)} sources found, press any key...')
input()


all_sd = []             # All source directory information

for s in source_dirs[:]:
    obs_dirs    = glob(f'{s}*/')

    sd = {}
    sd['dir']         = s
    sd['source_name'] = s.split('/')[-2]
    sd['n_obs']       = len(obs_dirs)
    sd['filesize']    = get_size(s)
    sd['filesize_gb'] = sd['filesize'] * 1e-9
    
    print(sd)
    all_sd.append(sd)

    """
    for o in obs_dirs:
        od = {}
        od['dir'] = o
        od['obsid'] = o.split('/')[-2]


        globs = ['*_sk*', '*.img']
        for g in globs:
            od[f'n_{g}') = len(

        od['n_*.sk']
        od['filesize'] = get_size(o)
        print(od)
    """

df = pd.DataFrame(all_sd)
print(df.sort_values('n_obs', ascending=False)

savepath = 'tables/query_local_sources.csv'
print(f'Saving source details to : {savepath}')
df.to_csv(savepath)

