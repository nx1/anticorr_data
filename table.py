table_names = {'earnshaw_summary',
               'hecarte_summary',
               'query_local_sources',
               'numaster_n_obs',
               'nustarmaster',
               'swiftmaster_summary',
               'walton_summary',
               'xmmmaster_n_obs',
               'xmmmaster',
               'UVOT_N_OBS',
               'UVOT_FLUX',
               'XRT_obs_rates',
               'closest_srcreg'}


class Table:
    def __init__(self, name, data):
        self.name = name
        self.OUTPATH_CSV = f'tables/csv/{self.name}.csv'
        self.OUTPATH_LATEX = f'tables/latex/{self.name}.tex'
        self.OUTPATH_FITS = f'tables/fits/{self.name}.fits'

    def load(self):

    def 
    
    def to_fits(self):
        outpath = f'{self.SAVEDIR_FITS}/{self.name}.fits'
        print(f'Saving to: {outpath}')

    def to_csv(self):
        outpath = f'{self.SAVEDIR_CSV}/{self.name}.csv'
        print(f'Saving to: {outpath}')

    def to_latex(self):
        outpath = f'{self.SAVEDIR_LATEX}/{self.name}.latex'
        print(f'Saving to: {outpath}')

    def save(self):
        self.to_fits()
        self.to_csv()
        self.to_latex()

if __name__ == "__main__":

for table_name in table_names:
    Table(table_name)

