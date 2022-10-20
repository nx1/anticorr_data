from pathlib import Path
import sys
import os
from itertools import combinations, product
sys.path.append('../')

import papermill as pm

from source_names_dict import source_names_dict
from uvot import filters
from xrt import curves

# Set output path
output_path = Path('correlation_outputs')

# Create list of parameters
#print(curves)
#print(filters)
incbad = [False, True]
incUL = [False, True]


combs = list(product(curves, filters, incbad, incUL))
source_names = list(source_names_dict.keys())
#print(combs)

#print(source_names_dict)

src_combs = list(product(source_names_dict, combs))

print('Creating param list...')
all_params = []
for simbad_name, par in src_combs:
    
    params = {}
    params['simbad_name'] = simbad_name
    params['xrt_curve']   = par[0]
    params['uvot_filter'] = par[1]
    params['include_bad'] = par[2]
    params['include_UL']  = par[3]
    params['outfile']     = f'{simbad_name},{par[0]},{par[1]},{par[2]},{par[3]}'
    
    all_params.append(params)
    #print(params)
    
print(f'Total Simulations: {len(all_params)}')
print(f'Expected run time = 5x{len(all_params)}/3600 = {5*len(all_params)/3600:.2f} hrs')
print('Press any key to run...')
input()


def run_notebook(params):
    print(params)
    out_nb = output_path/f'{params["outfile"]}.ipynb'
    if os.path.exists(out_nb):
        print(f'{out_nb} exists! skipping...')
        return 'exists'
    out_nb = output_path/f'{params["outfile"]}.ipynb'
    try:
        pm.execute_notebook('correlation_blueprint_with_UL.ipynb', out_nb, parameters=params)
        return 'success'
    except:
        return 'error'

rets = []
#ret = run_notebook(all_params[852])
#ret = run_notebook(all_params[853])

for i, params in enumerate(all_params):
    print(f'{i}/{len(all_params)}')
    ret = run_notebook(params)
    rets.append(ret)