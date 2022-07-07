from glob import glob
import linecache
import pandas as pd


def get_table_line_numbers(path):
    """Find the start and end line numbers of numerical data in a given path.
    
    Returns list of tuples:
         ('s/e', index)
        [('start',13), ('end',13), ]
    """
    with open(path, 'r') as f:
        data = f.readlines()

    last = None
    linenums = []

    for i, l in enumerate(data):
        current = l[0].isnumeric()
        if (last != current) & (last != None):
            # Start or end of numerical group detected
            #print(f'{i} {last} {current}')
            if (current==True) & (last==False):
                # Start of group
                linenums.append(('start',i))
            elif (current==False) & (last==True):
                # End of group
                linenums.append(('end',i))
            # print(linenums)
        last = current
    return linenums

def get_table_names(path):
    linenums = get_table_line_numbers(path)
    tab_names = []
    for l in linenums:
        if l[0] == 'start':
            # get the two lines proceeding the table
            line_1 = linecache.getline(path, l[1])
            line_2 = linecache.getline(path, l[1]-1)
            
            # print(l[1], line_1, line_2)
            
            # Get the table name
            for line in [line_1, line_2]:
                if 'WT data' in line:
                    tab_name = 'WT'
                elif 'PC data' in line:
                	tab_name = 'PC'
                elif 'PC upper limits' in line:
                	tab_name = 'PC_UL'
                elif 'WT upper limits' in line:
                	tab_name = 'WT_UL'
                elif 'WT -- hard data' in line:
                	tab_name = 'WT_HARD'
                elif 'WT -- soft data' in line:
                	tab_name = 'WT_SOFT'
                elif 'WT -- hardness ratio' in line:
                	tab_name = 'WT_HR'
                elif 'PC -- hard data' in line:
                	tab_name = 'PC_HARD'
                elif 'PC -- soft data' in line:
                	tab_name = 'PC_SOFT'
                elif 'PC -- hardness ratio' in line:
                	tab_name = 'PC_HR'
                else:
                	#print('No table name found in line!')
                	#print(line)
                	continue
                #print(f'tab_name = {tab_name}')
                tab_names.append(tab_name)
    return tab_names




def read_qdp(path):
    """
    Read .qdp files into pandas dataframe (https://wwwastro.msfc.nasa.gov/qdp/)
    Does not add the column names 
    
    returns
    -------
    dfs : list 
        - list of dataframes
    """
    ln = get_table_line_numbers(path)
    #print(path)
    #print(f'line numbers found: {ln}')
    #print('==============')
    nrows = None

    dfs = []
    for i in range(len(ln)):
        #print(i, ln[i])
        if ln[i][0] == 'start':
            start = ln[i][1]
            try:
                if ln[i+1][0] == 'end':
                    end = ln[i+1][1]
            except IndexError:
                end = None
            try:
                nrows = end - start
            except TypeError:
                nrows = None

            #print(start, end, nrows)
            df = pd.read_csv(path, skiprows=start, nrows=nrows, sep='\t', index_col=False, header=None)
            dfs.append(df)
    return dfs

if __name__ == "__main__":
    qdp_hardrat        = glob('UKSSDC/*/*/*/*hardrat.qdp')
    qdp_hardrat_incbad = glob('UKSSDC/*/*/*/*hardrat_incbad.qdp')
    qdp_curve          = glob('UKSSDC/*/*/*/*curve.qdp')
    qdp_curve_incbad   = glob('UKSSDC/*/*/*/*curve_incbad.qdp')
    qdp_nosys          = glob('UKSSDC/*/*/*/*curve_nosys.qdp')
    qdp_nosys_incbad   = glob('UKSSDC/*/*/*/*curve_nosys_incbad.qdp')


    for f in qdp_hardrat:
        dfs = read_qdp(f)
        tab_names = get_table_names(f)

        print(f'{f:<80} n_dfs = {len(dfs)}')
        print(tab_names)
        for df in dfs:
            print(df)
            input()


