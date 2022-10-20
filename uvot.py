import logging
from glob import glob
import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table
from astropy.time import Time

from source_names_dict import source_names_dict
from get_closest_srcreg import get_src_region_dict
from xrt import log_flag_summary 


def calc_uvot_flags(table):
    table['FLAG_AB_MAG_99']      = table['AB_MAG'] == 99
    table['FLAG_UPPER_LIM']      = table['NSIGMA'] < table['MAG_LIM_SIG'] 
    table['FLAG_AB_MAG_ERR>2']   = table['AB_MAG_ERR'] > 2
    table['FLAG_AB_MAG_>10_<30'] = np.logical_or((table['AB_MAG'] < 10), (table['AB_MAG'] > 30))

    flags = ['FLAG_AB_MAG_99', 'FLAG_UPPER_LIM', 'FLAG_AB_MAG_ERR>2', 'FLAG_AB_MAG_>10_<30']
    for f in flags:
        log_flag_summary(table, f)
    return table


def load_uvotsource(simbad_name, src_region_dict, filter_flags=True):
    local_name = source_names_dict[simbad_name]
    closest_src   = src_region_dict[simbad_name]
    fits_files = glob(f'/mnt/d/anticorr_data/download_scripts/{local_name}/*uvotsource*fits*')
    logging.debug(f'Loading uvotsource simbad_name={simbad_name} filter_flags={filter_flags}')
    for f in fits_files:
        if closest_src.split('/')[-1][:-4] in f:
            tab_uvot = read_uvotsource(f, filter_flags)
            return tab_uvot

def read_uvotsource(path, filter_flags=True):
    logging.debug('Reading uvotsource...')
    logging.debug(f'Reading file {path}')
    tab = Table.read(path)
    n_unique_obs = len(np.unique(tab['OBSID']))
    logging.debug(f'tab len={len(tab)} unique_obs={n_unique_obs}')
    
    tab.sort('MET')
    MJDREFI = 51910
    tab['MJD'] = MJDREFI  + tab['MET'] / 86400.0
    tab['YEAR'] = Time(np.array(tab['MJD']), format='mjd').decimalyear
    tab['MJD_0'] = tab['MJD'] - tab['MJD'].min()
    
    tab = calc_uvot_flags(tab)
    if filter_flags:
        logging.debug('Filtering out flags')
        tab = tab[~tab['FLAG_AB_MAG_99']]
        tab = tab[~tab['FLAG_UPPER_LIM']]
        tab = tab[~tab['FLAG_AB_MAG_ERR>2']]
    return tab


filters = ['B', 'U', 'V', 'UVM2', 'UVW1', 'UVW2', 'WHITE']

# Filter bandpass information https://swift.gsfc.nasa.gov/proposals/tech_appd/swiftta_v12/node39.html
# The centroid positions here may be slightly different as I think i got them from a diffeerent paper.
# All values are provided in Angstroms.
# See also http://svo2.cab.inta-csic.es/svo/theory/fps3/index.php?id=Swift/UVOT.V&&mode=browse&gname=Swift&gname2=UVOT#filter

filter_cent = {'B'    : 4392,
               'U'    : 3465,
               'V'    : 5468,
               'UVW1' : 2600,
               'UVM2' : 2246,
               'UVW2' : 1928,
               'WHITE': 3471}

filter_fwhm = {'B'    : 975,
               'U'    : 785,
               'V'    : 769,
               'UVW1' : 693,
               'UVM2' : 498,
               'UVW2' : 687,
               'WHITE': 6400}
               
filter_ref   = {'U' : 3467.05,
                'B' : 4349.56,
                'V' : 5411.43,
                'UVW1' : 2580.75,
                'UVM2' : 2246.43,
                'UVW2' : 2054.61}

filter_W_eff   = {'U' : 662.50,
                 'B'  : 866.22,
                 'V'  : 655.67,
                 'UVW1' : 801.92,
                 'UVM2' : 533.85,
                 'UVW2' : 667.73}

filter_colors = {'B'    : 'steelblue',
                 'U'    : 'indigo',
                 'V'    : 'green',
                 'UVW1' : 'cyan',
                 'UVM2' : 'magenta',
                 'UVW2' : 'orange',
                 'WHITE': 'gray'}

filter_markers = {'B'    : '.',
                  'U'    : 'v',
                  'V'    : '^',
                  'UVM2' : 's',
                  'UVW1' : 'x',
                  'UVW2' : '+',
                  'WHITE': '*'}

filter_rsp = {'B'       : Table.read('/mnt/d/anticorr_data/external/swift_rsp/b.rsp'), 
              'U'       : Table.read('/mnt/d/anticorr_data/external/swift_rsp/u.rsp'),    
              'V'       : Table.read('/mnt/d/anticorr_data/external/swift_rsp/v.rsp'),     
              'UVM2'    : Table.read('/mnt/d/anticorr_data/external/swift_rsp/uvm2.rsp'),   
              'UVW1'    : Table.read('/mnt/d/anticorr_data/external/swift_rsp/uvw1.rsp'),      
              'UVW2'    : Table.read('/mnt/d/anticorr_data/external/swift_rsp/uvw2.rsp'),    
              'WHITE'   : Table.read('/mnt/d/anticorr_data/external/swift_rsp/white.rsp'),
              'U_GRISM' : Table.read('/mnt/d/anticorr_data/external/swift_rsp/ugrism.rsp'),
              'V_GRISM' : Table.read('/mnt/d/anticorr_data/external/swift_rsp/vgrism.rsp')}


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        datefmt='%H:%M:%S',
                        format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s')

    src_region_dict = get_src_region_dict()
    for simbad_name, local_name in source_names_dict.items():
        try:
            tab = load_uvotsource(simbad_name, src_region_dict, filter_flags=True)
        except Exception as e:
            print(f'{simbad_name} {e}')

