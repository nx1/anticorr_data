from glob import glob

sh_file = 'ds9_uvot.sh'
source_dirs = glob('download_scripts/*/')

cmd_lines = []
for s in source_dirs:
    img_files = glob(f'{s}*uuu.img')
    region_files   = glob(f'{s}*.reg')

    for img in img_files:
        if 'sky' in img:
            source_name = s.split('/')[-2]
            region_files   = glob(f'{s}*.reg')
            cmd = f'ds9 -log -cmap invert {img}'

            if len(region_files) > 0:
                for reg in region_files:
                    reg_fn = reg
                    cmd += f' -region {reg_fn}'
 
            print(cmd)
            cmd_lines.append(cmd)


print(f'Writing {len(cmd)} commands to: {sh_file}')
with open(sh_file, 'w+') as f:
    for l in cmd_lines:
        f.write(f'{l} & \n')
