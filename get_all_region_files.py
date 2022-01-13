from glob import glob
import pandas as pd
import astropy.units as u
from astropy.coordinates import SkyCoord

def get_all_regions():
    reg_files = glob('download_scripts/*/*.reg')
    
    all_regs = []
    
    for r in reg_files:
        with open(r, 'r') as f:
            lines = f.readlines()
    
        reg_dict = {}
        for l in lines:
            if 'circle' in l:
                reg = l.replace('\n','')
                ra, dec, radius = reg.replace('circle(','').replace(')','').split(',')
                reg_dict['path'] = r
                reg_dict['region'] = reg
                reg_dict['ra'] = ra
                reg_dict['dec'] = dec
                reg_dict['radius'] = radius
                sc = SkyCoord(ra, dec,
                              unit=(u.hourangle, u.deg),
                              frame='fk5')
                reg_dict['ra_deg']   = sc.ra.deg
                reg_dict['dec_deg']  = sc.dec.deg
                reg_dict['skycoord'] = sc

        all_regs.append(reg_dict)
    
    df = pd.DataFrame(all_regs)
    return df

if __name__ == "__main__":
    df = get_all_regions()
    print(df)
