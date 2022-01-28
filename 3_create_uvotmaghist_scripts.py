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
    src_reg_files = glob(f'{s}*src*.reg')

    maghist_lines = []
    for infile in maghist_files:
        infile = '/'.join(infile.split('/')[2:])

        for src in src_reg_files:
            srcreg = src.split('/')[-1]
            outfile = infile[:-7] + '_' + srcreg[:-4] + '_maghist.fits'
            maghist_line = f'uvotmaghist infile={infile} outfile={outfile} srcreg={srcreg} bkgreg=bkg.reg plotfile=NONE\n'
            maghist_lines.append(maghist_line)

    print(f'Creating {uvotmaghist_sh_path:<60} lines={len(maghist_lines)}')
    with open(uvotmaghist_sh_path, 'w+') as f:
        for l in maghist_lines:
            f.write(f'{l}')


sh_path = 'uvotmaghist_all_sources.sh'
print(f'Creating {sh_path}')
with open(sh_path, 'w+') as f:
    for l in all_uvotmaghist_paths:
        f.write(f'{l}\n')
