# 9_create_source_lightcurves.py
# outputs to lightcurves/
# SOURCE_NAME_UVOT_U_SRC_UVOTALL.FITS
# SOURCE_NAME_UVOT_UW1_SRC_UVOTALL.FITS
# SOURCE_NAME_XRT_FULL.FITS
# SOURCE_NAME_XRT_HARD.FITS


# 09_create lightcurves
# 10_linear_correlation.py
# 11_lomb_scargle_lightcurves.py
# 12_cross_correlation.py
# 


from glob import glob
import numpy as np

import pandas as pd
from astropy.table import Table
import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.table import vstack, hstack, join, unique
from astroquery.simbad import Simbad

from source_names_dict import source_names_dict

def get_src_region_dict(return_df=False):
    # Fix glob square bracket issue
    to_replace = {'[':'[[]',
                  ']':'[]]'}
    
    
    # Associate Source files with nearsest SIMBAD ID
    
    src_region_dict = {}
    all_dicts = []
    s = Simbad
    for simbad_name, local_name in source_names_dict.items():
        print(f'{simbad_name:<50}{local_name}')
        min_sep_file = ''
        min_sep = 9999*u.deg
        
        tab = s.query_object(simbad_name)
        sc1 = SkyCoord(tab['RA'][0], tab['DEC'][0], unit=(u.hourangle, u.deg))
        
        
        src_reg_files = glob(f'/mnt/d/anticorr_data/download_scripts/{local_name}/*src*.reg*')
        for r in src_reg_files:
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
                    sc2 = SkyCoord(ra, dec,
                                  unit=(u.hourangle, u.deg),
                                  frame='fk5')
                    
            sep = sc1.separation(sc2)
            if sep < min_sep:
                min_sep = sep
                min_sep_file = r
            #print(f'{simbad_name:<30} {r} Seperation = {sep}')
        
        dict2 = {}
        dict2['simbad_name'] = simbad_name
        dict2['local_name']  = local_name
        dict2['simbad_sc']   = sc1
        dict2['simbad_ra']   = sc1.ra
        dict2['simbad_dec']  = sc1.dec
        dict2['local_sc']    = sc2
        dict2['local_ra']    = sc2.ra
        dict2['local_dec']   = sc2.dec
        dict2['closest_srcreg'] = min_sep_file
        dict2['closest_srcreg_sep_deg'] = min_sep
        dict2['closest_srcreg_sep_arcsec'] = min_sep.to("arcsec")
        all_dicts.append(dict2)
    
        src_region_dict[simbad_name] = min_sep_file

    assert len(src_region_dict) == len(np.unique(src_region_dict.items())[0]) # Make sure no duplicate src regions
    
    df = pd.DataFrame(all_dicts)
    if return_df:
        return src_region_dict, df
    else:
        return src_region_dict


if __name__ == "__main__":
    src_region_dict, df = get_src_region_dict(return_df=True)

    print(df[['simbad_name', 'local_name', 'simbad_ra', 'simbad_dec', 'local_ra', 'local_dec', 'closest_srcreg', 'closest_srcreg_sep_arcsec']].sort_values('closest_srcreg_sep_arcsec', ascending=False))
