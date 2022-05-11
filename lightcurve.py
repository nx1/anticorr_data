import numpy as np
from scipy.stats import skew, kurtosis
import matplotlib.pyplot as plt

from lomb_scargle import Lomb_Scargle

def get_gtis(t):
    diff = np.diff(t)
    mu   = np.mean(diff)
    #lo  = mu - np.std(diff)
    hi   = mu + np.std(diff)

    max_diff = hi
    
    if len(diff) > 10:
        gap_indexs = []
        for i, val in enumerate(diff):
            # print(f'i={i} t[i]={t[i]:.2f}')
            if val > max_diff:
                # print(f'i={i} t[i]={t[i]:.2f} max diff exceeded! val>max_diff ({val:.2f}>{hi:.2f})')
                gap_indexs.append([i, i+1])

        # Turn the bad intervals into good intervals                        
        gti_indexs = []
        first = [0, gap_indexs[0][0]] # Get the gti for the data at the start
        gti_indexs.append(first)

        for i in range(len(gap_indexs)-1):
            #print([0, gti_indexs[i][0]])
            term = [gap_indexs[i][1], gap_indexs[i+1][0]]
            gti_indexs.append(term)
        
        last = [gap_indexs[-1][1], len(t)-1] # get the gtis for the data at the end
        gti_indexs.append(last)

        gtis = [[int(t[s]), int(t[e])+1] for s, e in gti_indexs]
        #print(gti_indexs)
        #print(gtis)
        return gti_indexs, gtis
    else:
        return [], []
    
def calc_von_neumann_stat(y):
    """
    Ann. Math. Statist. 12(4): 367-395 (December, 1941).
    dio: 10.1214/aoms/1177731677
    
    see also: https://ui.adsabs.harvard.edu/abs/2018MNRAS.481..307K/abstract
    """
    y = np.array(y)
    if len(y) < 2:
        return 99
    
    s2 = np.var(y)
    n = len(y)
    eta = ((1 / (n-1)) * np.sum((y[1:] - y[:-1])**2)) / s2
    return eta


def calc_sigma_xs(y, y_err):
    """Calculate the excess variance.
    See equation (8) and (9)
    https://ui.adsabs.harvard.edu/abs/2003MNRAS.345.1271V/abstract
    """
    y = np.array(y)
    y_err = np.array(y_err)
    if len(y) < 2:
        return 99
    N = len(y)
    sigma_err_2 = (1/N) * np.sum(y_err**2)
    S2 = np.var(y, ddof=1)    # See equation (6)
    sigma_xs = S2 - sigma_err_2
    return sigma_xs


def calc_F_var(y, y_err):
    """Calculate the fractional variance"""
    y = np.array(y)
    y_err = np.array(y_err)
    if len(y) < 2:
        return 99
    N = len(y)
    sigma_err_2 = (1/N) * np.sum(y_err**2)
    S2 = np.var(y, ddof=1)    # See equation (6)
    F_var = np.sqrt((S2 - sigma_err_2) / np.mean(y)**2)
    return F_var


class LightCurve:
    def __init__(self, t, y, y_err):
        self.t     = t
        self.y     = y
        self.y_err = y_err
        self.name  = ''

    def set_name(self, name):
        self.name = name

    def calc_t_diff(self):
        self.t_diff = np.diff(self.t)

    def calc_y_diff(self):
         self.y_diff = np.diff(self.y)

    @property
    def gtis(self):
        print('Getting lightcurve gtis...')
        return get_gtis(self.t)
    
    @property
    def sigma_xs(self):
        return calc_sigma_xs(self.y, self.y_err)
    
    @property
    def F_var(self):
        return calc_F_var(self.y, self.y_err)
    
    @property
    def kurtosis(self):
        return kurtosis(self.y)
    
    @property
    def von_neumann(self):
        return calc_von_neumann_stat(self.y)
    
    @property
    def skew(self):
        return skew(self.y)
    
    def lomb_scargle(self):
        self.ls = Lomb_Scargle(self.t, self.y, self.y_err)
        self.ls.run()
        
    def analyse(self):
        res = {}
        res['ndata']       = len(self.y)
        res['mean']        = np.mean(self.y)
        res['std']         = np.std(self.y)
        res['max']         = np.max(self.y)
        res['min']         = np.min(self.y)
        res['max/min']     = res['max'] / res['min']
        res['sigma_xs']    = self.sigma_xs
        res['F_var']       = self.F_var
        res['kurtosis']    = self.kurtosis
        res['von_neumann'] = self.von_neumann
        res['skew']        = self.skew

        self.calc_t_diff()
        res['t_diff_max']  = np.max(self.t_diff)
        res['t_diff_min']  = np.min(self.t_diff)
        res['t_diff_mean'] = np.mean(self.t_diff)

        self.calc_y_diff()
        res['y_diff_max']  = np.max(self.y_diff)
        res['y_diff_min']  = np.min(self.y_diff)
        res['y_diff_mean'] = np.mean(self.y_diff)
       
        self.lomb_scargle()
        if self.ls.success:
            print('LS success')
            res['ls_z_fal'] = self.ls.z_fal
            for i in range(self.ls.npeaks):
                res[f'ls_pow[{i}]']    = self.ls.max_powers[i]
                res[f'ls_freq[{i}]']   = self.ls.max_freqs[i]
                res[f'ls_period[{i}]'] = self.ls.max_periods[i]
                res[f'ls_fap[{i}]']    = self.ls.fap_bootstraps[i]
        else:
            print('LS failed')
            res['ls_z_fal']        = None
            for i in range(self.ls.npeaks):
                res[f'ls_pow[{i}]']    = None
                res[f'ls_freq[{i}]']   = None
                res[f'ls_period[{i}]'] = None
                res[f'ls_fap[{i}]']    = None
        return res
    
    
    def plot(self):
        plt.figure(figsize=(15,5))
        plt.errorbar(self.t, self.y, yerr=self.y_err, ls='none', lw=1.0, capsize=1.0, marker='.')
        if self.name != '':
            plt.title(self.name)
            plt.savefig(f'../figures/lcs/curves/{self.name}.png')
            plt.savefig(f'../figures/lcs/curves/{self.name}.pdf')
        plt.show()
        
    def plot_no_gaps(self):
        plt.figure(figsize=(15,5))
        plt.errorbar(range(len(self.y)), self.y, yerr=self.y_err, ls='none', lw=1.0, capsize=1.0, marker='.')
        if self.name != '':
            plt.title(self.name)
            plt.savefig(f'../figures/lcs/curves_no_gaps/{self.name}.png')
            plt.savefig(f'../figures/lcs/curves_no_gaps/{self.name}.pdf')
        plt.show()
    
    def plot_lomb_scargle(self):
        if self.ls.success:
            plt.figure(figsize=(10,5))
            plt.plot(self.ls.frequency, self.ls.power)
            for i in range(self.ls.npeaks):
                plt.axvline(self.ls.max_freqs[i], color='red', ls='dotted', lw=2.0, label=f'i={i} freq={self.ls.max_freqs[i]:.2e} (P={self.ls.max_periods[i]:.2f})')

            # plot the false-alarm levels
            plt.axhline(self.ls.z_fal, linestyle='dotted', color='black', label=fr'$\sigma$ = {self.ls.z_fal:.2f} ({self.ls.false_alarm_lvl*100}%)')
            plt.legend()
            if self.name != '':
                plt.title(f'Lomb Scargle {self.name}')
                plt.xlabel('Frequency (1/days)')
                plt.savefig(f'../figures/lcs/lomb_scargle/{self.name}.png')
                plt.savefig(f'../figures/lcs/lomb_scargle/{self.name}.pdf')
            plt.show()

    def plot_all(self):
        self.plot()
        self.plot_no_gaps()
        self.plot_lomb_scargle()
        plt.show()
        
