from glob import glob
from astropy.table import Table

for f in glob('external/*/*.fits'):
        tab = Table.read(f)
        csv_name = f[:-5]+'.csv'
        print(f'{f:<100} --> {csv_name}')
        tab.write(csv_name, format='csv')
