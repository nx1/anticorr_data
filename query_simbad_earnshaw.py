from astropy.table import Table
from astroquery.simbad import Simbad

cat = Table.read('external/Earnshaw_ULX_cat/earnshaw_Xraycatalogue.fits')

source_names = cat['IAUNAME']

s = Simbad()
s.add_votable_fields('distance')
tab = s.query_objects(source_names)
#tab['SEARCH_NAME'] = source_names

print(tab)
print(len(tab),len(cat))
#assert len(tab) == len(source_names)

tab.write('tables/query_simbad_earnshaw.csv', overwrite=True)
col_subset = ['RA','DEC', 'COO_BIBCODE']
tab[col_subset].write('tables/query_simbad_earnshaw.tex', format='latex', overwrite=True)


