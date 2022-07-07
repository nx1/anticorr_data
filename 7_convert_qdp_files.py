import linecache
from glob import glob
import pandas as pd
import qdp

def process_qdp(path, cols, obsid_col):
    """
    Path : path to qdp file
    cols : column names to use
    obsid_col : does the table have obsids in it?
    """
    dfs = qdp.read_qdp(path) 
    tab_names = qdp.get_table_names(path)
    
    for i, df in enumerate(dfs):
        df.columns = cols
        if obsid_col:
            df['obsID'] = df['obsID'].str.extract(r'(\d{11})')   # Uncomment for old curves
        fn = f'{path[:-4]}_{tab_names[i]}.csv'
        print(f'Saving file to {fn}')
        df.to_csv(fn, index=False)
        print('='*50)
    
def process_qdps(paths, cols, obsid_col):
    for p in paths:
        process_qdp(p, cols, obsid_col)

if __name__ == "__main__":

    qdp_curve          = glob('UKSSDC/*/*/*/*curve.qdp')
    qdp_curve_incbad   = glob('UKSSDC/*/*/*/*curve_incbad.qdp')
    qdp_hardrat        = glob('UKSSDC/*/*/*/*hardrat.qdp')
    qdp_hardrat_incbad = glob('UKSSDC/*/*/*/*hardrat_incbad.qdp')
    qdp_nosys          = glob('UKSSDC/*/*/*/*curve_nosys.qdp')
    qdp_nosys_incbad   = glob('UKSSDC/*/*/*/*curve_nosys_incbad.qdp')


    cols_curve          = ['MJD', 'T_+ve', 'T_-ve', 'Rate', 'Ratepos', 'Rateneg']
    cols_curve_incbad   = ['MJD', 'T_+ve', 'T_-ve', 'Rate', 'Ratepos', 'Rateneg']
    cols_hardrat        = ['MJD', 'Err (pos)', 'Err(neg)', 'Rate', 'Error', 'obsID']
    cols_hardrat_incbad = ['MJD', 'Err (pos)', 'Err(neg)', 'Rate', 'Error', 'obsID']
    cols_nosys          = ['MJD', 'T_+ve', 'T_-ve', 'Rate', 'Ratepos', 'Rateneg', 'obsID']
    cols_nosys_incbad   = ['MJD', 'T_+ve', 'T_-ve', 'Rate', 'Ratepos', 'Rateneg', 'obsID']

    print('Files to process:')
    print(f'curve.qdp              : {len(qdp_curve)}')
    print(f'curve_incbad.qdp       : {len(qdp_curve_incbad)}')
    print(f'hardrat.qdp            : {len(qdp_hardrat)}')
    print(f'hardrat_incbad.qdp     : {len(qdp_hardrat_incbad)}')
    print(f'curve_nosys.qdp        : {len(qdp_nosys)}')
    print(f'curve_nosys_incbad.qdp : {len(qdp_nosys_incbad)}')
    print('Press any key to start...')
    input()

    process_qdps(qdp_curve,          cols_curve          , False)
    process_qdps(qdp_curve_incbad,   cols_curve_incbad   , False)
    process_qdps(qdp_hardrat,        cols_hardrat        , True)
    process_qdps(qdp_hardrat_incbad, cols_hardrat_incbad , True)
    process_qdps(qdp_nosys,          cols_nosys          , True)
    process_qdps(qdp_nosys_incbad,   cols_nosys_incbad   , True)
    
    
