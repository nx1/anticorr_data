import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R
from area import Model

if __name__ == "__main__":
    x0, y0, z0 = 0.0, 0.0, 1.0
    star_pos_init = np.array([x0, y0, z0])
    
    res = []
    
    for phase_ang in np.arange(0,20,0.1):
        rot = R.from_euler('xyz', [0, phase_ang, 0], degrees=True)
        star_pos_rot = rot.apply(star_pos_init)
        
        mo_input = {'theta' : 20.0,
                    'x0' : star_pos_rot[0],
                    'y0' : star_pos_rot[1],
                    'z0' : star_pos_rot[2],
                    'r'  : 10.0,
                    'i'  : 10.0,
                    'mask_z':True}
                    

        mo = Model(**mo_input)
        mo.run()
        mo.plot()
        mo.print()
        out = mo.collect()
        out['phase_ang'] = phase_ang
        res.append(out)
        
    df_res = pd.DataFrame(res)
    
    
    # Create Results DataFrames
    df_res  = pd.DataFrame(res)
    print(df_res)
    
    # Calculate secondary quantities
    df_res['area_star_2d'] = np.pi * df_res['r']**2
    df_res['area_ratio_irr_star'] = df_res['area_irr_proj'] / df_res['area_star_2d']
    
    
    print(df_res)

    plt.figure(figsize=(6,6))
    plt.plot(df_res['phase_ang'], df_res['area_ratio_irr_star'], color='red')
    plt.xlabel('Phase Angle')
    plt.ylabel(r'Irradiated Fraction (A / $\pi r^2$)')
    
    plt.savefig('plt_out/phase_vs_area.png')
    plt.show()
    