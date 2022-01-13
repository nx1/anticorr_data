from glob import glob
import pandas as pd

source_dirs = glob('download_scripts/*/')

all_res = []

for s in source_dirs:
    
    obs_dirs = glob(f'{s}*/')
    for obs in obs_dirs:
        res = {}
        res['source_name'] = s.split('/')[1]
        res['observation'] = obs.split('/')[-2]
        res['date'] = 
        all_res.append(res)

df = pd.DataFrame(all_res)
print(df)
