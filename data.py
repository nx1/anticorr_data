import logging
from astropy.table import unique, join

from source_names_dict import source_names_dict
from xrt import load_xrt, rename_xrt_cols
from uvot import load_uvotsource
from table_closest_srcreg import get_src_region_dict 

def load_joined(simbad_name, xrt_curve, uvot_filter, src_region_dict, join_hr=False):
    # Load X-ray Data
    tab_xrt_full = load_xrt(simbad_name=simbad_name, curve=xrt_curve, pandas=False)
    print(tab_xrt_full)
    tab_xrt_full = rename_xrt_cols(tab_xrt_full)

    # Load UVOT Data
    tab_uvot = load_uvotsource(simbad_name, src_region_dict)
    tab_uvot = tab_uvot[tab_uvot['FILTER'] == uvot_filter]
    tab_uvot = unique(tab_uvot, keys='OBSID')

    # Join Data
    tab_join = join(tab_uvot, tab_xrt_full , join_type='inner', keys='OBSID')
    tab_join.sort('MJD_0_1')

    if join_hr:
       tab_xrt_hr = load_xrt(simbad_name, 'HR', pandas=False)
       tab_join2 = join(tab_join, tab_xrt_hr, join_type='inner', keys='OBSID')
       return tab_join2

    return tab_join


if __name__ == "__main__":
    src_region_dict = get_src_region_dict()
    xrt_curve='PC'
    uvot_filter='U'
    for simbad_name, local_name in source_names_dict.items():
        print(f'simbad_name={simbad_name} xrt_curve={xrt_curve} uvot_filter={uvot_filter}')
        try:
            df_joined = load_joined(simbad_name, xrt_curve, uvot_filter, src_region_dict)
            df_joined.pprint(max_lines=-1, max_width=-1)
        except Exception as e:
            print(f'{simbad_name:<40} {e}')

