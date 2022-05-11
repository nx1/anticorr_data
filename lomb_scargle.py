import numpy as np
from scipy.signal import find_peaks
import astropy.units as u
from astropy.timeseries import LombScargle

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
    if len(y) < 2:
        return 99
    N = len(y)
    sigma_err_2 = (1/N) * np.sum(y_err**2)
    S2 = np.var(y, ddof=1)    # See equation (6)
    sigma_xs = S2 - sigma_err_2
    return sigma_xs


def calc_F_var(y, y_err):
    """Calculate the fractional variance"""
    if len(y) < 2:
        return 99
    N = len(y)
    sigma_err_2 = (1/N) * np.sum(y_err**2)
    S2 = np.var(y, ddof=1)    # See equation (6)
    F_var = np.sqrt((S2 - sigma_err_2) / np.mean(y)**2)
    return F_var



class Lomb_Scargle:
    def __init__(self, t, y, y_err):
        self.t     = np.array(t)
        self.y     = np.array(y)
        self.y_err = np.array(y_err)
        self.ls = LombScargle(self.t, self.y, self.y_err)
        self.false_alarm_lvl = 0.01
        self.min_freq = 1 / 1000 
        self.max_freq = 1
        self.npeaks   = 3 # Return top n peaks
        self.max_powers         = np.empty(self.npeaks)
        self.max_freqs          = np.empty(self.npeaks)
        self.max_periods        = np.empty(self.npeaks)
        self.fap_bootstraps     = np.empty(self.npeaks)
        self.success            = False


    def run(self):
        print('Calculating Lomb scargle periodogram using autopower')
        self.frequency, self.power = self.ls.autopower(minimum_frequency=self.min_freq, maximum_frequency=self.max_freq)
        print(f'min(frequency) = {min(self.frequency):.2f} max(frequency) = {max(self.frequency):.2f}')
        self.z_fal  = self.ls.false_alarm_level(self.false_alarm_lvl, method='bootstrap')
        
        # Find peaks
        distance = int(len(self.frequency) * 0.025)
        peak_idx, peaks_dict = find_peaks(self.power, height=self.z_fal.value/2, distance=distance)
        n_found_peaks = len(peak_idx)
        if n_found_peaks  >= 1:
            loop_peaks = self.npeaks
            # Sort peak ids by height (descending)
            peak_heights_sorted = -np.sort(-peaks_dict['peak_heights'])
            peak_idx_sorted     = np.flip([x for _, x in sorted(zip(peaks_dict['peak_heights'], peak_idx))])
            
            # if we found less than npeaks just return the ones we got
            if n_found_peaks < self.npeaks:
                loop_peaks = n_found_peaks
            
                
            # Iterate over n most siginificant peaks
            for i in range(loop_peaks):
                power = peak_heights_sorted[i]
                idx   = peak_idx_sorted[i]
                freq   = self.frequency[idx]
                period = 1 / freq
                fap    = self.ls.false_alarm_probability(power, method='bootstrap')

                self.max_powers[i]     = power
                self.max_freqs[i]      = freq
                self.max_periods[i]    = period
                self.fap_bootstraps[i] = fap
                print(f'pow={power:.2f} freq={freq:.2e} p={period:.2f} fap={fap:.2f}')
            self.success = True
        else:
            print('No peaks found')
            self.success = False