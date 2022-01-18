from source_names import source_names
from astroquery.simbad import Simbad


s = Simbad()
tab = s.query_objects(source_names)
tab['SEARCH_NAME'] = source_names

print(tab)
assert len(tab) == len(source_names)
