from glob import glob
import pandas as pd

source_dirs = glob('download_scripts/*/')

all_res = []

all_uvotmaghist_paths = []

for s in source_dirs:
    uvotsource_sh_path = s + 'uvotsource_all.sh'
    all_uvotmaghist_paths.append(uvotsource_sh_path)
    img_files = glob(f'{s}*/*_sk.img.gz')
    src_reg_files = glob(f'{s}*src*.reg')

    maghist_lines = []
    for infile in img_files:
        infile = '/'.join(infile.split('/')[2:])
        imsum_outfile = infile[:-7] +'_imsum.img.gz'
        imsum_line = f'uvotimsum infile={infile} outfile={imsum_outfile}\n'
        maghist_lines.append(imsum_line)

        for src in src_reg_files:
            srcreg = src.split('/')[-1]
            outfile = imsum_outfile[:-7] + '_' + srcreg[:-4] + '_uvotsource.fits'
            maghist_line = f'uvotsource image={imsum_outfile} outfile={outfile} srcreg={srcreg} bkgreg=bkg.reg sigma=3.0\n'
            maghist_lines.append(maghist_line)

    print(f'Creating {uvotsource_sh_path:<60} lines={len(maghist_lines)}')
    with open(uvotsource_sh_path, 'w+') as f:
        for l in maghist_lines:
            f.write(f'{l}')


sh_path = 'uvotsource_all_sources.sh'
print(f'Creating {sh_path}')

with open(sh_path, 'w+') as f:
    for l in source_dirs:
        f.write(f'cd {l}\n')
        f.write(f'./uvotsource_all.sh & \n')
        f.write('cd ../..\n')
