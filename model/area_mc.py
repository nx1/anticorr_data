from itertools import product
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.spatial.transform import Rotation as R
from area import Model

grid_mc = {'theta'  : [5,10,20],
           'x0'     : [0],
           'y0'     : [0],
           'z0'     : [1, 10, 50],
		   'r'      : [1, 10, 20],
		   'i'      : [0, 10, 20, 45],
		   'mask_z' : [True]}
           
           
grid_params     = list(grid_mc.keys())                      # list of 'str' containing param names
grid_N_params   = len(grid_mc)                              # Number of parameters
grid_iterations = sum([len(i) for i in grid_mc.values()]) # number of grid iterations
grid_product    = product(*grid_mc.values())                # Gridsearch Iterator

all_res = []
iteration = 0
for v in grid_product:
    params = {} # Array for storing current iteration sim params

    # Populate param_dict
    for i in range(grid_N_params):
        param_name = grid_params[i]
        param_val  = v[i]
        params[param_name] = param_val

    star_pos_init = np.array([params['x0'], params['y0'], params['z0']])
    
    # Simulate transit
    for phase_ang in np.arange(0,50,5.0):
        rot = R.from_euler('xyz', [0, phase_ang, 0], degrees=True)
        star_pos_rot = rot.apply(star_pos_init)
        params['x0'] = star_pos_rot[0]
        params['y0'] = star_pos_rot[1]
        params['z0'] = star_pos_rot[2]

        m = Model(**params)
        m.run()
        #m.print()
        res = m.collect()
        res['phase_ang'] = phase_ang
        res['iteration'] = iteration
        all_res.append(res)
        #print(res)
        
    iteration+=1
    print(iteration)
df_res = pd.DataFrame(all_res)

print(df_res)
fn = 'mc_output.csv'
print(f'Saving output to: {fn}')
df_res.to_csv(fn)