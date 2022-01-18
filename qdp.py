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


