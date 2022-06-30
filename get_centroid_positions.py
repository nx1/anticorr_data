import re
import pandas as pd
import matplotlib.pyplot as plt
from glob import glob

lcgen_files = glob('UKSSDC/*/*/*/*lcgen.log')

all_res = []
for fn in glob('UKSSDC/*/*/*/*lcgen.log'):
    print(fn)

    sp = fn.split('/')
    simbad_name = sp[1]
    

    # fn = '/mnt/d/anticorr_data/UKSSDC/NAME_NGC_1313_X-2/USERPROD_45605/lc/lcgen.log'
    with open(fn,'r') as f:
        data = f.readlines()
    
    
    
    
    for i, l in enumerate(data):
        if 'Centroid output' in l:
           print('Found Centroid output!')
           print(i, l)
           # print(data[i+1])
           print(data[i+2])
           if 'No source centroid found' in data[i+2]:
                continue
           regex = re.findall(r"[-+]?\d*\.?\d+|\d+", data[i+2])
           # print(res)
           ra = regex[0]
           dec = regex[1]
           print(ra, dec)
    
           res = {}
           res['ra'] = float(ra)
           res['dec'] = float(dec)
           res['simbad_name'] = simbad_name

    
        if "Running 'xrtinstrmap_0.3.5'" in l:
            print('found xrtinstrmap!!')
            print(data[i+5])
            regex = re.findall(r"\d{11}", data[i+5])
            obsid = regex[0]
            try:
                res['obsid'] = obsid
            except NameError:
                continue
            print(res)
            all_res.append(res)
    print(fn)

df = pd.DataFrame(all_res)
df = df.drop_duplicates()
print(df)

savepath = 'tables/xrt_centroids.csv'
print(f'Saving to: {savepath}')
df.to_csv(savepath, index=False)



df.plot(kind='scatter', x='ra', y='dec')
plt.show()
