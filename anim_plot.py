import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib as mpl
from matplotlib.collections import LineCollection
from mpl_toolkits.axes_grid1 import make_axes_locatable

from astropy.table import unique, join

from table_closest_srcreg import get_src_region_dict
from source_names_dict import source_names_dict, source_names_w_counterparts, source_names_readable
from uvot import load_uvotsource, calc_uvot_flags, filters, filter_colors, filter_markers
from xrt import load_xrt, rename_xrt_cols

parser = argparse.ArgumentParser()
parser.add_argument('simbad_name', help='Simbad Name of source')               
parser.add_argument('xrt_curve',   help='UVOT filter to use.')                 
parser.add_argument('uvot_filter', help='XRT curve to use.')                   
args = parser.parse_args()


 
simbad_name = args.simbad_name
local_name  = source_names_dict[simbad_name]
readable_name = source_names_readable[simbad_name]


src_region_dict = get_src_region_dict()

uvot_filter = args.uvot_filter
xrt_curve = args.xrt_curve

xrt_rate      = 'RATE'
xrt_rate_err  = 'RATE_ERR'

uvot_rate     = 'COI_SRC_RATE'
uvot_rate_err = 'COI_SRC_RATE_ERR'

# Load X-ray Data
tab_xrt_full = load_xrt(simbad_name=simbad_name, curve=xrt_curve, pandas=False)
tab_xrt_full = rename_xrt_cols(tab_xrt_full)

tab_xrt_hr   = load_xrt(simbad_name, 'HR', pandas=False)

# Load UV Data
tab_uvot = load_uvotsource(simbad_name, src_region_dict)
tab_uvot = tab_uvot[tab_uvot['FILTER'] == uvot_filter]
tab_uvot = unique(tab_uvot, keys='OBSID')

print(tab_uvot)
# Join Data
tab_join = join(tab_uvot, tab_xrt_full , join_type='inner', keys='OBSID')
print(tab_join)
tab_join.sort('MJD_0_1')

tab_join2 = join(tab_join, tab_xrt_hr, join_type='inner', keys='OBSID')

# Get x,y data
t = tab_join['MJD_0_1']

x = tab_join[uvot_rate]
x_err = tab_join[uvot_rate_err]

y = tab_join[xrt_rate]
y_err = tab_join[xrt_rate_err]

size  = len(x)

# get HR data
hr     = tab_join2['RATE_2']
hr_err = tab_join2['RATE_ERR_2']

##########################################
################# PLOTTING ###############
##########################################

# Set up HR colormap
cmap = mpl.cm.coolwarm
norm = mpl.colors.TwoSlopeNorm(vmin=min(hr), vcenter=1, vmax=max(hr))


fig, ax = plt.subplots(4,1, figsize=(5,10), gridspec_kw={'height_ratios': [1,1,1,3]})

ax[0].set_title(f'{readable_name} | UVOT={uvot_filter} XRT={xrt_curve}')

# Plot Temporal Lightcurve
ax[0].errorbar(t, x, yerr=x_err, label='UVOT', color='purple',
                       capsize=1.0, lw=1.0, ls='none')
ax4 = ax[0].twinx()
ax4.errorbar(t, y, yerr=y_err, label='XRT', color='black',
                       capsize=1.0, lw=1.0, ls='none')

ax[0].set_xlabel(f'MJD - {tab_join["MJD_1"].min()}')
ax[0].set_ylabel(uvot_rate)
ax4.set_ylabel(xrt_rate)


ax[1].plot(x, label='UVOT', color='purple')
ax3 = ax[1].twinx()
ax3.plot(y, label='XRT', color='gray')

vl = ax[1].axvline(0, ls='-', color='r', lw=1)    
vl2 = ax[0].axvline(0, ls='-', color='r', lw=1)    


ax[1].set_ylabel(uvot_rate)
ax3.set_ylabel(xrt_rate)


# Plot HR values
ax[2].errorbar(range(len(hr)), hr, yerr=hr_err, label='HR', color='black', capsize=1.0, lw=1.0, ls='none')
vl3 = ax[2].axvline(0, ls='-', color='r', lw=1)    
ax[2].set_ylabel('HR RATIO')



# Plot Correlation
ax[3].scatter(x, y, marker='x', color='grey', alpha=0.5)

points = np.array([x,y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)
lc = LineCollection(segments)

ax[3].add_collection(lc)

ax[3].set_xlim(np.mean(x) - 2*np.std(x), np.mean(x) + 2*np.std(x))
ax[3].set_ylim(np.mean(y) - 2*np.std(y), np.mean(y) + 2*np.std(y))

ax[3].set_xlabel(uvot_rate)
ax[3].set_ylabel(xrt_rate)

# Add colorbar
divider = make_axes_locatable(ax[3])
cax = divider.append_axes('right', size='5%', pad=0.05)
fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), cax=cax,
             orientation='vertical', label='HR')


def animate(i, vl):
    vl.set_xdata([i,i])
    vl2.set_xdata([t[i],t[i]])
    vl3.set_xdata([i,i])
     
    sl = 30 # Show last n points
    lc.set_segments(segments[:i])

    if i < sl:
        lc.set_segments(segments[:i])
        lc.set_colors(cmap(norm(hr[:i])))
    if i >= sl:
        lc.set_segments(segments[i-sl:i])
        lc.set_colors(cmap(norm(hr[i-sl:i])))
    return vl, vl2, vl3, lc

ani = animation.FuncAnimation(fig, animate, fargs=[vl], interval=80, blit=True,
                              save_count=50, repeat=True, frames=size)

plt.tight_layout()
from matplotlib.animation import PillowWriter
ani.save(f'figures/corr_anim/{simbad_name},{xrt_curve},{uvot_filter}.gif', writer=PillowWriter(fps=20))
#plt.show()
#plt.close()
