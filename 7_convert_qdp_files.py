from glob import glob
import qdp
import pandas as pd

curve_qdps   = glob('UKSSDC/*/*USERPROD*/*/*curve.qdp')
hardrat_qdps = glob('UKSSDC/*/*USERPROD*/*/*hardrat.qdp')

print('Files to process:')
print(f'curve.qdp : {len(curve_qdps)} \t hardrat.qdp : {len(hardrat_qdps)}')
print('Press any key to start...')

input()

# read all files of the form `curve.qdp'
for f in curve_qdps:
    colnames = ['MJD', 'T_+ve', 'T_-ve', 'Rate', 'Ratepos', 'Rateneg', 'obsID']
    dfs = qdp.read_qdp(f) # if two dfs : first table WT mode 2nd PO mode
    print(f)

    for i, df in enumerate(dfs):
        df.columns = colnames
        df['obsID'] = df['obsID'].str.extract(r'(\d{11})')
        # print(df)
        if len(dfs) == 2:
            if i == 0:
                print(f'Saving file to {f[:-4]+"_WT.csv"}')
                df.to_csv(f[:-4]+'_WT.csv', index=False)
            elif i == 1:
                print(f'Saving file to {f[:-4]+"_PC.csv"}')
                df.to_csv(f[:-4]+'_PC.csv', index=False)
        else:
            print(f'Saving file to {f[:-4]+"_PC.csv"}')
            df.to_csv(f[:-4]+'_PC.csv', index=False) # THIS MAY ACTUALLY BE WT in some cases (rare)
    print('-'*50)

# read all files of type `hardrat.qdp'
for f in hardrat_qdps:
    dfs = qdp.read_qdp(f)
    colnames = ['MJD', 'Err (pos)', 'Err(neg)', 'Rate', 'Error', 'obsID']
    lctypes = ['HARD', 'SOFT', 'HR']

    print(f'{f} \t {len(dfs)}')
    for i, df in enumerate(dfs):
        # get mode
        if len(dfs) == 3:
            mode = 'PC'
        elif len(dfs) == 6:
            if i <= 2:
                mode = 'WT'
            elif i >= 3:
                mode = 'PC'

        # get soft/hard or HR
        lctype = lctypes[i%3]
        df.columns = colnames
        df['obsID'] = df['obsID'].str.extract(r'(\d{11})')
        fn = f[:-4] +f'_{lctype}_{mode}.csv'
        print(f'Saving file to {fn}')
        df.to_csv(fn, index=False)
    print('-'*50)

