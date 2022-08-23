import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from area import Model

if __name__ == "__main__":
    mo_input = {'theta':15.0,
                'x0':1.0,
                'y0':1.0,
                'z0':4.0,
                'r':3,
                'i':7.4,
                'mask_z':True}

    # Lists for storing results
    res = []

    for i in np.arange(0,90,1):
        #mo_input['x0'] = x0
        mo_input['i'] = i
        
        mo = Model(**mo_input)
        
        print(mo)
        mo.run()
        mo.plot()
        out = mo.collect()
        # Print 
        for k, v in mo.__dict__.items():
            print(f'{str(type(v)):<25} {k:<20} : {v}')
        
        print('='*150)
        res.append(out)
        
    
    # Create Results DataFrames
    df_res  = pd.DataFrame(res)
    print(df_res)
    
    # Calculate secondary quantities
    
    df_res['area_star_2d'] = np.pi * df_res['r']**2
    
    df_res['area_ratio_irr_star'] = df_res['area_irr_proj'] / df_res['area_star_2d']
    
    
    print(df_res)

    plt.figure(figsize=(6,6))
    plt.plot(df_res['i'], df_res['area_ratio_irr_star'], color='red')
    plt.xlabel('Inclination (i)')
    plt.ylabel(r'Irradiated Fraction (A / $\pi r^2$)')
    
    plt.savefig('plt_out/incl_vs_area.png')
    plt.show()
    