from astroquery.simbad import Simbad
from source_names_dict import source_names_dict

source_names = list(source_names_dict.keys())

s = Simbad()
s.add_votable_fields('distance')
tab = s.query_objects(source_names)
tab['SEARCH_NAME'] = source_names

print(tab)
assert len(tab) == len(source_names)

tab.write('tables/query_simbad.csv', overwrite=True)
col_subset = ['SEARCH_NAME','RA','DEC', 'COO_BIBCODE']
tab[col_subset].write('tables/query_simbad.tex', format='latex', overwrite=True)

