from glob import glob
import pandas as pd

source_dirs = glob('download_scripts/*/')

all_imsum_paths = []

for s in source_dirs:
    imsum_sh_path = s + 'imsum_all.sh'
    all_imsum_paths.append(imsum_sh_path)

    """
    d = {'sk_img_u.txt'   :glob(f'{s}*/*[1]u_sk.img.gz'),
         'sk_img_uuu.txt' :glob(f'{s}*/*uuu_sk.img.gz'),
         'sk_img_uw1.txt' :glob(f'{s}*/*uw1_sk.img.gz'),
         'sk_img_uw2.txt' :glob(f'{s}*/*uw2_sk.img.gz'),
         'sk_img_um2.txt' :glob(f'{s}*/*um2_sk.img.gz'),
         'sk_img_ubb.txt' :glob(f'{s}*/*ubb_sk.img.gz'),
         'sk_img_uvv.txt' :glob(f'{s}*/*uvv_sk.img.gz')}   

    # Create txt files with each line containing sk_img file
    for k, v in d.items():
        txt_path = s+k
        print(f'Creating {txt_path:<50} lines={len(v)}')
        with open(txt_path, 'w+') as f:
            for l in v:
                stem = '/'.join(l.split('/')[2:])
                f.write(f'{stem}\n')
    """

    # Create the source imsum script
    source_imsum_sh_path = s + 'imsum_all.sh'
    print(f'Creating {source_imsum_sh_path}')
    with open(source_imsum_sh_path, 'w+') as f:
        f.write('#uvotimsum infile=@sk_img_u.txt outfile=sky_img_u.img\n')
        f.write('#uvotimsum infile=@sk_img_uuu.txt outfile=sky_img_uuu.img\n')
        f.write('#iuvotimsum infile=@sk_img_uw1.txt outfile=sky_img_uw1.img\n')
        f.write('uvotimsum infile=@sk_img_uw2.txt outfile=sky_img_uw2.img\n')
        f.write('uvotimsum infile=@sk_img_um2.txt outfile=sky_img_um2.img\n')
        f.write('#uvotimsum infile=@sk_img_ubb.txt outfile=sky_img_ubb.img\n')
        f.write('#uvotimsum infile=@sk_img_uvv.txt outfile=sky_img_uvv.img')



    
sh_path = 'imsum_all_sources.sh'
print(f'Creating {sh_path}')
with open(sh_path, 'w+') as f:
    for l in source_dirs:
        f.write(f'cd {l}\n')
        f.write('./imsum_all.sh\n')
        f.write('cd ../..\n')
