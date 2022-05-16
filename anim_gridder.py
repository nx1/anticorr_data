from itertools import combinations, product

from source_names_dict import source_names_w_counterparts
from uvot import filters
from xrt import curves


curves.remove('HR')

combs = list(product(curves, filters))
print(combs)
print(source_names_w_counterparts)

src_combs = list(product(source_names_w_counterparts, combs))

all_params = []

outfile = 'anim_gridder.sh'
with open(outfile, 'w+') as f:
    for simbad_name, lc in src_combs:
        params = {}
        params['simbad_name'] = simbad_name
        params['xrt_curve'] = lc[0]
        params['uvot_filter'] = lc[1]
        all_params.append(params)
        #print(params)
        line = f'python3 anim_plot.py {simbad_name} {lc[0]} {lc[1]} \n'
        print(line)
        f.write(line)

print(f'File written to: {outfile}')
