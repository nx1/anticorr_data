from glob import glob
import matplotlib.pyplot as plt
import pandas as pd


source_dirs = glob('UKSSDC/*/')

# Fix glob square bracket issue
to_replace = {'[':'[[]',
              ']':'[]]'}


for s in source_dirs:
    s_esc = s.translate(str.maketrans(to_replace))
    curve_files = glob(f'{s_esc}*/*/*curve_PC.csv')
    print(s)
    for f in curve_files:
        df = pd.read_csv(f, dtype={'obsID':'string'})
        print(f)
        print(df)

