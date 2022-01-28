from glob import glob
from shutil import unpack_archive

tar_gz_files = glob('UKSSDC/*/*.tar.gz')

print(f'Found {len(tar_gz_files)} tar.gz files')

# Unzip all tar_gz files
for f in tar_gz_files:
    extract_path = '/'.join(f.split('/')[:-1])
    print(f'Unzipping {f:<80} extract path:{extract_path}')
    unpack_archive(f, extract_path)
