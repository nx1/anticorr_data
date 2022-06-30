from glob import glob
import numpy as np

import pandas as pd
from astropy.table import Table
import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.table import vstack, hstack, join, unique
from astroquery.simbad import Simbad

from source_names_dict import source_names_dict, source_names_readable


def read_region_file(path):
    with open(path, 'r') as f:
        lines = f.readlines()
        
    reg_dict = {}
    for l in lines:
        if 'circle' in l:
            reg = l.replace('\n','')
            ra, dec, radius = reg.replace('circle(','').replace(')','').split(',')
            reg_dict['path'] = path
            reg_dict['region'] = reg
            reg_dict['ra'] = ra
            reg_dict['dec'] = dec
            reg_dict['radius'] = radius
            sc = SkyCoord(ra, dec,
                           unit=(u.hourangle, u.deg),
                                  frame='fk5')
    return reg_dict, sc

def get_src_region_dict(return_df=False):
    print('Getting source region dict')
    # Fix glob square bracket issue
    to_replace = {'[':'[[]',
                  ']':'[]]'}
    
    
    # Associate Source files with nearsest SIMBAD ID
    
    src_region_dict = {}
    all_dicts = []
    s = Simbad
    for simbad_name, local_name in source_names_dict.items():
        readable_name = source_names_readable[simbad_name]
        # print(f'{simbad_name:<50}{local_name}')
        min_sep_file = ''
        min_sep = 9999*u.deg
        
        tab = s.query_object(simbad_name)
        sc1 = SkyCoord(tab['RA'][0], tab['DEC'][0], unit=(u.hourangle, u.deg))
        
        
        src_reg_files = glob(f'/mnt/d/anticorr_data/download_scripts/{local_name}/*src*.reg*')
        bkg_reg_file  = glob(f'/mnt/d/anticorr_data/download_scripts/{local_name}/*bkg*.reg*')[0]

        for r in src_reg_files:
            reg_dict, sc2 = read_region_file(r)
            sep = sc1.separation(sc2)
            if sep < min_sep:
                min_sep = sep
                min_sep_file = r
            #print(f'{simbad_name:<30} {r} Seperation = {sep}')

        reg_dict_bkg, sc_bkg = read_region_file(r)

        
        dict2 = {}
        dict2['simbad_name'] = simbad_name
        dict2['local_name']  = local_name
        dict2['readable_name'] = readable_name
        dict2['simbad_sc']   = sc1
        dict2['simbad_ra']   = sc1.ra
        dict2['simbad_dec']  = sc1.dec
        dict2['local_sc']    = sc2
        dict2['local_ra']    = sc2.ra
        dict2['local_dec']   = sc2.dec
        dict2['closest_srcreg'] = min_sep_file
        dict2['closest_srcreg_short'] = '/'.join(min_sep_file.split('/')[-2:])
        dict2['closest_srcreg_sep_deg'] = min_sep
        dict2['closest_srcreg_sep_arcsec'] = min_sep.to("arcsec")
        dict2['bkg_srcreg'] = bkg_reg_file
        dict2['bkg_sc']     = sc_bkg
        dict2['bkg_ra']     = sc_bkg.ra
        dict2['bkg_dec']    = sc_bkg.dec
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
    print(df[['simbad_name', 'local_name', 'readable_name', 'simbad_ra', 'simbad_dec', 'local_ra', 'local_dec', 'closest_srcreg_short', 'closest_srcreg_sep_arcsec', 'bkg_ra', 'bkg_dec']].sort_values('closest_srcreg_sep_arcsec', ascending=False))
