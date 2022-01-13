from glob import glob
import pandas as pd

source_dirs = glob('download_scripts/*/')

all_res = []

for s in source_dirs:
    res = {}
    
    obs_dirs = glob(f'{s}*/')
    n_obs = len(obs_dirs)

    res['source_name'] = s.split('/')[1]
    res['n_obs'] = n_obs
    all_res.append(res)

df = pd.DataFrame(all_res)
df = df.sort_values('n_obs', ascending=False, ignore_index=True)
print(df)
