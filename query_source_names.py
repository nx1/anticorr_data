from source_names import source_names
from astroquery.simbad import Simbad

tab = Simbad.query_objects(source_names)

tab['search_name'] = source_names
print(tab)
assert len(tab) == len(source_names)
