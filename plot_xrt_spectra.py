"""
Plot XRT spectra
using pyXSPEC
"""
import os
from glob import glob
import matplotlib.pyplot as plt
from xspec import Spectrum, Plot, AllData
from source_names_dict import source_names_readable


source_dirs = glob('/mnt/d/anticorr_data/UKSSDC_spec/*/')

print(f'Source directories = {len(source_dirs)}')
print('Press any key to start...')
input()

def get_spec(source_dir):
    os.chdir(source_dir)
    if not os.path.exists('interval0pc.pi'):
        print(f'{source_dir} interval0pc.pi not found')
        os.chdir('/mnt/d/anticorr_data/')
        return 0,0,0,0
    spec = Spectrum('interval0pc.pi')
    spec.ignore('bad')

    
    Plot.device = '/xw'
    Plot.xAxis = 'keV'
    Plot.setRebin(minSig=3, maxBins=5, groupNum=1)
    Plot('ldata')
    x, y, x_err, y_err = Plot.x(), Plot.y(), Plot.xErr(), Plot.yErr()
    AllData.clear()
    os.chdir('/mnt/d/anticorr_data/')
    return x, y, x_err, y_err

def get_simbad_name(source_dir):
    return source_dir.split('/')[-2]

fig, axes = plt.subplots(7,5, figsize=(20,28))

i = 0
for source_dir in source_dirs:
    ax = axes.flatten()[i]
    x, y, x_err, y_err = get_spec(source_dir)
    simbad_name = get_simbad_name(source_dir)
    readable_name = source_names_readable[simbad_name]
    if x!=0:
        ax.errorbar(x,y,xerr=x_err,yerr=y_err, ls='none', label=readable_name)
        i+=1

for ax in axes.flatten():
    ax.set_yscale('log')
    ax.set_xlim(0.2,10.0)
    ax.legend()
    ax.set_xlabel('Energy (keV)')
    ax.set_ylabel(r'Counts $\mathrm{s}^{-1} \ \mathrm{keV}^{-1}$')

plt.savefig('figures/all_spectra.png', bbox_inches='tight')
plt.savefig('figures/all_spectra.pdf', bbox_inches='tight')
plt.show()


