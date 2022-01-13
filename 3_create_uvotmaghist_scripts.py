"""
create_uvot_maghist_scripts.py
"""
from glob import glob
import pandas as pd

source_dirs = glob('download_scripts/*/')

all_res = []

all_uvotmaghist_paths = []

for s in source_dirs:
    uvotmaghist_sh_path = s + 'uvotmaghist_all.sh'
    all_uvotmaghist_paths.append(uvotmaghist_sh_path)
    maghist_files = glob(f'{s}*/*_sk.img.gz')

    maghist_lines = []
    for infile in maghist_files:
        infile = '/'.join(infile.split('/')[2:])
        outfile = infile[:-7] + '_maghist.fits'
        maghist_line = f'uvotmaghist infile={infile} outfile={outfile} srcreg=src.reg bkgreg=bkg.reg plotfile=NONE\n'
        maghist_lines.append(maghist_line)

    print(f'Creating {uvotmaghist_sh_path} \t lines={len(maghist_lines)}')
    with open(uvotmaghist_sh_path, 'w+') as f:
        for l in maghist_lines:
            f.write(f'{l}')

sh_path = 'uvotmaghist_all_sources.sh'
print(f'Creating {sh_path}')
with open(sh_path, 'w+') as f:
    for l in all_uvotmaghist_paths:
        f.write(f'{l}\n')
