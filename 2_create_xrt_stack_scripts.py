from glob import glob
import pandas as pd

source_dirs = glob('download_scripts/*/')

all_sh_paths = []

for s in source_dirs:
    xcm_path    = s + 'xrt_stack.xcm'
    xrt_sh_path = s + 'xrt_stack.sh'
    xrt_po_txt_path = s + 'xrt_cl_evt.txt'

    all_sh_paths.append(xrt_po_txt_path)

    xrt_po_files = glob(f'{s}*/*po_cl.evt.gz') # get all xrt pointing files
    # Create txt files with each line containing sk_img file
    print(f'Creating {xrt_po_txt_path} \t files_to_stack={len(xrt_po_files)}')
    xrt_po_files = xrt_po_files[:500] # can only load 500 files in at once in xselect
    with open(xrt_po_txt_path, 'w+') as f:
        for l in xrt_po_files:
            stem = '/'.join(l.split('/')[2:])
            f.write(f'{stem}\n')

    # Create the source imsum script
    print(f'Creating {xcm_path}')
    with open(xcm_path, 'w+') as f:
        f.write('session\n')
        f.write(f'read events @xrt_cl_evt.txt\n')
        f.write('./\n')
        f.write('y\n')
        f.write('extract image\n')
        f.write('save image xrt_stack.img\n')
        f.write('exit\n')
        f.write('n')

    # Create sh file to call xselect
    print(f'Creating {xrt_sh_path}')
    with open(xrt_sh_path, 'w+') as f:
        f.write(f'xselect @xrt_stack.xcm')

   
sh_path = 'xrt_stack_all_sources.sh'
print(f'Creating {sh_path}')
with open(sh_path, 'w+') as f:
    for l in source_dirs:
        f.write(f'cd {l}\n')
        f.write('./xrt_stack.sh\n')
        f.write('cd ../..\n')

