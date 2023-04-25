"""Create Host distance Table"""

from astroquery.simbad import Simbad
from astropy.table import join
import astropy.units as u

from source_names_dict import source_names_dict, source_names_readable

source_names = list(source_names_dict.keys())
gal_names = list(source_names_dict.values())
source_names_r = list(source_names_readable.values())
print(len(source_names), len(gal_names), len(source_names_r))

tab1 = Simbad.query_objects(source_names)
tab1['source_name'] = source_names
tab1['source_name_readable'] = source_names_r

print('tab1:')
print(tab1)

Simbad.add_votable_fields('distance')

tab = Simbad.query_objects(gal_names)
tab['source_name'] = source_names
print('tab:')
print(tab)

sub = tab['MAIN_ID', 'Distance_distance', 'Distance_unit', 'Distance_method', 'Distance_bibcode', 'source_name']
sub.sort('Distance_distance')


tab_join = join(tab1,tab, keys='source_name')
print('tab_join:')
print(tab_join)

print(tab_join[['source_name', 'Distance_distance']])


sub_cols     = ['source_name_readable', 'RA_1', 'DEC_1', 'COO_WAVELENGTH_1', 'COO_BIBCODE_1', 'Distance_distance', 'Distance_unit', 'Distance_method', 'Distance_bibcode']
sub_cols_new = ['source_name',          'RA',   'DEC',   '$\lambda$',        'POS_REF',       'D',                 'D_unit',        'D_method',        'D_ref']
sub = tab_join[sub_cols]
sub.rename_columns(names=sub_cols, new_names=sub_cols_new)
sub['D'].unit = u.Mpc
sub.sort('D')
print('sub:')
print(sub)

outfile_source_with_hosts = 'tables/source_with_hosts.tex'
outfile_source_with_hosts_csv = 'tables/source_with_hosts.csv'


# sub.write(outfile_source_with_hosts, format='latex', overwrite=True)
sub.write(outfile_source_with_hosts_csv, format='csv', overwrite=True)
