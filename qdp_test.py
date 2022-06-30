from glob import glob
from qdp import read_qdp, get_table_line_numbers

if __name__ == "__main__":
    qdp_files = glob('UKSSDC/NAME_NGC_1313_X-1/USERPROD_60932/lc/*.qdp')
    print(f'# qdp files = {len(qdp_files)}')
    print('Press any key to start')
    # input()
    for f in qdp_files:
        linenums = get_table_line_numbers(f)
        print(linenums)
        dfs = read_qdp(f)
        print(f)
        for df in dfs:
            print(df)
        input()
