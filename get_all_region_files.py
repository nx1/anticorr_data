from glob import glob
import pandas as pd
import astropy.units as u
from astropy.coordinates import SkyCoord

def get_all_regions():
    reg_files = glob('download_scripts/*/*.reg')
    
    all_regs = []
    
    for r in reg_files:
        with open(r, 'r') as f:
            lines = f.readlines()
    
        reg_dict = {}
        for l in lines:
            if 'circle' in l:
                reg = l.replace('\n','')
                ra, dec, radius = reg.replace('circle(','').replace(')','').split(',')
                reg_dict['path'] = r
                reg_dict['path_fn'] = r.split('/')[-1][:-4]
                reg_dict['local_name'] = r.split('/')[1]
                reg_dict['region'] = reg
                reg_dict['ra'] = ra
                reg_dict['dec'] = dec
                reg_dict['radius'] = radius
                sc = SkyCoord(ra, dec,
                              unit=(u.hourangle, u.deg),
                              frame='fk5')
                reg_dict['ra_deg']   = sc.ra.deg
                reg_dict['dec_deg']  = sc.dec.deg
                reg_dict['skycoord'] = sc

        all_regs.append(reg_dict)
    
    df = pd.DataFrame(all_regs)
    df = df.dropna()
    return df

def reshape_df_reg(df):
    df_src = df[df['path'].str.contains('src')]
    df_bkg = df[df['path'].str.contains('bkg')]
    df_new = df_src.merge(df_bkg, how='outer', on='local_name', suffixes=('_src', '_bkg'))
    return df_new

if __name__ == "__main__":
    df = get_all_regions()

    pd.set_option('display.max_rows', None)
    print(df[['path','ra','dec','radius']])

    df_src_bkg = reshape_df_reg(df)
    outcols = ['local_name','path_fn_src','ra_src','dec_src', 'radius_src','ra_bkg', 'dec_bkg','radius_bkg']
    print(df_src_bkg[outcols])
    latex_outfile = 'tables/src_bkg_reg.tex'
    print(f'Saving to {latex_outfile}')
    df_src_bkg[outcols].to_latex(latex_outfile, index=False)
    
    #df_bkg = df[df['path'].str.contains('bkg')]
    #df_src = df[df['path'].str.contains('src')]
