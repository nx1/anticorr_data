from glob import glob
from tqdm import tqdm
import pandas as pd

def load_df_prop():
    all_df = []
    for f in tqdm(glob('/mnt/d/anticorr_data/lightcurves/correlation_output/*/tables/*table_prop*')):
        sp = f.split('/')[-1].split(',')
        simbad_name = sp[0]
        xrt_curve   = sp[1]
        uvot_filter = sp[2]
        include_bad = sp[3]
        include_UL  = sp[4]

        df = pd.read_csv(f)
        df['simbad_name'] = simbad_name
        df['xrt_curve'] = xrt_curve
        df['uvot_filter'] = uvot_filter
        df['include_bad'] = include_bad
        df['include_UL']  = include_UL

        all_df.append(df)
    df_prop = pd.concat(all_df)
    df_prop_idx = df_prop.set_index(['simbad_name','xrt_curve', 'uvot_filter', 'include_bad', 'include_UL', 'name'])
    return df_prop
    
def load_df_fit_samples():
    all_dfs = []
    for f in tqdm(glob('/mnt/d/anticorr_data/lightcurves/correlation_output/*/tables/*table_corr*')):
        sp = f.split('/')[-1].split(',')
        simbad_name = sp[0]
        xrt_curve   = sp[1]
        uvot_filter = sp[2]
        include_bad = sp[3]
        include_UL  = sp[4]

        df = pd.read_csv(f)
        df['simbad_name'] = simbad_name
        df['xrt_curve'] = xrt_curve
        df['uvot_filter'] = uvot_filter
        df['include_bad'] = include_bad
        df['include_UL'] = include_UL
        all_dfs.append(df)
    df_fit_samples = pd.concat(all_dfs)
    return df_fit_samples
    
def load_df_fit_values():
    all_res = []
    for f in tqdm(glob('/mnt/d/anticorr_data/lightcurves/correlation_output/*/tables/*table_corr*')):
        sp = f.split('/')[-1].split(',')
        simbad_name = sp[0]
        xrt_curve   = sp[1]
        uvot_filter = sp[2]
        include_bad = sp[3]
        include_UL  = sp[4]
        
        # print(simbad_name, xrt_curve, uvot_filter)
        
        df = pd.read_csv(f)
        r_mean = df['r'].mean()
        r_std  = df['r'].std()
        m_mean = df['m'].mean()
        m_std  = df['m'].std()
        c_mean = df['c'].mean()
        c_std  = df['c'].std()
        
        res = {}
        res['simbad_name'] = simbad_name
        res['xrt_curve'] = xrt_curve
        res['uvot_filter'] = uvot_filter
        res['include_bad'] = include_bad
        res['include_UL'] = include_UL
        
        res['r_mean'] = r_mean
        res['r_std'] = r_std
        res['m_mean'] = m_mean
        res['m_std'] = m_std
        res['c_mean'] = c_mean
        res['c_std'] = c_std
        
        all_res.append(res)
    df = pd.DataFrame(all_res)
    return df
