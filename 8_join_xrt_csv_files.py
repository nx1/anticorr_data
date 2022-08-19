from glob import glob
import pandas as pd
import matplotlib.pyplot as plt
import functools

import sys
sys.path.append('../')
from source_names_dict import source_names_dict


def get_csv_dict(csv_path):
    csv_dict = {}
    # Get path
    csv_dict['path'] = csv_path
    #csv_dict['df'] = pd.read_csv(csv_path, dtype={'obsID':str})
    
    csv_path = csv_path.split('/')[-1]
   
    # Get Prefix
    if 'curve_nosys' in csv_path:
        csv_dict['prefix'] = 'curve_nosys'
    elif 'hardrat' in csv_path:
        csv_dict['prefix'] = 'hardrat'
    
    # Get mode
    if 'PC' in csv_path:
        csv_dict['mode'] = 'PC'
    elif 'WT' in csv_path:
        csv_dict['mode'] = 'WT'
        
    # Get incbad
    if 'incbad' in csv_path:
        csv_dict['incbad'] = True
    elif 'incbad' not in csv_path:
        csv_dict['incbad'] = False
    
    # get UL
    if 'UL' in csv_path:
        csv_dict['UL'] = True
    elif 'UL' not in csv_path:
        csv_dict['UL'] = False
        
    # get band
    if 'HARD' in csv_path:
        csv_dict['band'] = 'HARD'
    elif 'SOFT' in csv_path:
        csv_dict['band'] = 'SOFT'
    elif 'HR' in csv_path:
        csv_dict['band'] = 'HR'
    else:
        csv_dict['band'] = 'FULL'
    return csv_dict

# Fix glob square bracket issue
to_replace = {'[':'[[]',
              ']':'[]]'}

for simbad_name, local_name in source_names_dict.items():
    simbad_name_glob = simbad_name.translate(str.maketrans(to_replace)) # Used to fix globbing square brackets
    curve_nosys_files = glob(f'UKSSDC/{simbad_name_glob}/*/*/*curve_nosys*.csv')
    hardrat_files     = glob(f'UKSSDC/{simbad_name_glob}/*/*/*hardrat*.csv')


    
    print(f'{simbad_name:<40} curve_nosys_files={len(curve_nosys_files)} hardrat_files={len(hardrat_files)}')
    
    if len(curve_nosys_files) == 0:
        print('No csv files, loop continue...')
        continue
    
    # Get CSV dicts
    curve_nosys_dicts = [get_csv_dict(csv) for csv in curve_nosys_files]
    hardrat_dicts     = [get_csv_dict(csv) for csv in hardrat_files]

    dfs_curve_nosys = []
    for d in curve_nosys_dicts:
        print(d)
        df = pd.read_csv(d['path'], dtype={'obsID':str})
        df['MODE'] = d['mode']
        df['BAD']  = d['incbad']
        df['UL']   = d['UL']
        df['BAND'] = d['band']
        dfs_curve_nosys.append(df)
        
    # Merge dataframes
    df_merge = functools.reduce(lambda left,right: pd.merge(left, right, how='outer'), dfs_curve_nosys)

    # Remove duplicate obsIDs, keeping values with bad == False
    df_merge = df_merge.sort_values('BAD')
    df_merge = df_merge.drop_duplicates('obsID', keep='first')

    # Re-sort by MJD
    df_merge = df_merge.sort_values('MJD').reset_index(drop=True)
    
    print(df_merge)
    curve_nosys_savefile = f'lightcurves/xrt/{simbad_name},curve_nosys_join.csv'
    print(f'Saving file to: {curve_nosys_savefile}')
    df_merge.to_csv(curve_nosys_savefile, index=False)
    
    
    print('-'*50 + ' NOW DOING HARDRAT' + '-'*50)
    
    
    dfs_hardrat = []
    for d in hardrat_dicts:
        print(d)
        df = pd.read_csv(d['path'], dtype={'obsID':str})
        df['MODE'] = d['mode']
        df['BAD']  = d['incbad']
        df['UL']   = d['UL']
        df['BAND'] = d['band']
        dfs_hardrat.append(df)
        
        
    # Merge dataframes
    df_merge = functools.reduce(lambda left,right: pd.merge(left, right, how='outer'), dfs_hardrat)
    print(df_merge)
    df_merge = df_merge.sort_values('BAD')
    df_merge = df_merge.drop_duplicates(['obsID', 'BAND'], keep='first')
    # Remove duplicate obsIDs, keeping values with bad == False
    # df_merge = df_merge.sort_values('BAD')
    # df_merge = df_merge.drop_duplicates('obsID', keep='first')

    # Re-sort by MJD
    df_merge = df_merge.sort_values('MJD').reset_index(drop=True)
    print(df_merge)

    curve_nosys_savefile = f'lightcurves/xrt/{simbad_name},hardrat_join.csv'
    print(f'Saving file to: {curve_nosys_savefile}')
    df_merge.to_csv(curve_nosys_savefile, index=False)
        
    
    print('='*100)
