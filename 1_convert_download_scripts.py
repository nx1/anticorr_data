"""Convert HEASARC swift download script to UKSSDC"""
import re
import glob

comp = re.compile(r'\d{11}')

def convert_script(script_path):
    script_path_no_sh = script_path[:-3]
    srcname = script_path_no_sh.split('/')[-1]
    out_path = script_path_no_sh + '_UKSSDC.sh'
    print(f'Converting script {script_path} --> {out_path}')

    with open(script_path, 'r') as f:
        lines = f.readlines()

    newlines = []
    for l in lines:
        if 'wget' in l[0:4]:
            obsid = comp.findall(l)[0]
            swift_url = f'https://www.swift.ac.uk/archive/reproc/{obsid}/'
            l_split = l.split(' ')
            l_split[-1] = swift_url
            l_split.append(f'-P {srcname}/{obsid}/')
            newline = ' '.join(l_split)
            newlines.append(newline)
            
    # Write outfile
    with open(out_path, 'w+') as f:
        for l in newlines:
            f.write('%s\n' % l)
            
            
if __name__ == "__main__":
    # Convert all files:
    scripts = glob.glob('download_scripts/*.sh')
    for s in scripts:
        if 'UKSSDC' not in s:
            convert_script(s)


    # Create download_all.sh
    download_all_path = 'download_scripts/download_all.sh'
    print(f'Creating run all script: {download_all_path}')

    scripts = glob.glob('download_scripts/*_UKSSDC.sh')
    script_filenames = [s.split('/')[-1] for s in scripts]
    with open(download_all_path, 'w+') as f:
        for s in script_filenames:
            f.write('./%s\n' % s)
