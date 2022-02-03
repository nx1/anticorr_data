from glob import glob

sh_file = 'ds9_xrt.sh'
source_dirs = glob('download_scripts/*/')

cmd_lines = []
for s in source_dirs:
    source_name = s.split('/')[-2]
    region_files   = glob(f'{s}*.reg')
    xrt_stack_files = glob(f'{s}*xrt_stack.img')
    
    if len(xrt_stack_files) > 0:
        fn = xrt_stack_files[0]
        # cmd = f'ds9 -log -cmap cool {fn}'
        cmd = f'ds9 -log -cmap invert {fn}'
        # cmd = f'ds9 -log -cmap cool -cmap invert {fn} -export png ds9/{source_name}.png'
        if len(region_files) > 0:
            for reg in region_files:
                reg_fn = reg
                cmd += f' -region {reg_fn}'
        print(cmd)
        cmd_lines.append(cmd)

print(f'Writing commands to: {sh_file}')
with open(sh_file, 'w+') as f:
    for l in cmd_lines:
        f.write(f'{l} & \n')
