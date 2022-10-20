from pathlib import Path
      

import sys
from itertools import combinations, product
sys.path.append('../')

import papermill as pm

from source_names_dict import source_names_w_counterparts
from uvot import filters
from xrt import curves

# Set output path
output_path = Path('correlation_outputs')

# Create list of parameters
print(curves)
print(filters)

combs = list(product(curves, filters))
print(combs)
print(source_names_w_counterparts)

src_combs = list(product(source_names_w_counterparts, combs))

all_params = []
for simbad_name, lc in src_combs:
    params = {}
    params['simbad_name'] = simbad_name
    params['xrt_curve'] = lc[0]
    params['uvot_filter'] = lc[1]
    params['outfile'] = f'{simbad_name},{lc[0]},{lc[1]}'
    all_params.append(params)
    print(params)

for i, params in enumerate(all_params):
    print(f'{i}/{len(all_params)}')
    try:
        pm.execute_notebook('correlation_blueprint.ipynb',
                            output_path/f'{params["outfile"]}.ipynb',
                            parameters=params)
    except:
        print(f'Error with {params}')
    
