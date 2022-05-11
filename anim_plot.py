import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from astropy.table import unique, join

from source_names_dict import source_names_dict, source_names_w_counterparts, source_names_readable
from uvot import read_uvotsource, calc_uvot_flags, filters, filter_colors, filter_markers
from xrt import load_xrt, rename_xrt_cols

simbad_name = 'NAME_NGC_1313_X-2'

local_name  = source_names_dict[simbad_name]
readable_name = source_names_readable[simbad_name]

uvot_filter = 'U'
xrt_curve = 'HARD'

xrt_rate      = 'RATE'
xrt_rate_err  = 'RATE_ERR'

uvot_rate     = 'COI_SRC_RATE'
uvot_rate_err = 'COI_SRC_RATE_ERR'

# Load X-ray Data
tab_xrt_full = load_xrt(simbad_name=simbad_name, curve=xrt_curve, pandas=False)
tab_xrt_full = rename_xrt_cols(tab_xrt_full)

# Load UV Data
tab_uvot = read_uvotsource(f'download_scripts/NGC1313/X-2_src_uvotsource_all.fits')
tab_uvot = tab_uvot[tab_uvot['FILTER'] == uvot_filter]
tab_uvot = unique(tab_uvot, keys='OBSID')

# Join Data
tab_join = join(tab_uvot, tab_xrt_full , join_type='inner', keys='OBSID')
tab_join.sort('MJD_0')

# Remove outlier
tab_join = tab_join[tab_join[uvot_rate] < 3]

# Get x,y data
t = tab_join['MJD_0']

x = tab_join[uvot_rate]
x_err = tab_join[uvot_rate_err]

y = tab_join[xrt_rate]
y_err = tab_join[xrt_rate_err]

size  = len(x)


# Plotting
fig, ax = plt.subplots(2,1)
line, = ax[1].plot(x[0], y[0])

line2 = ax[0].plot(x, label='UVOT', color='purple')
ax3 = ax[0].twinx()
ax[0].set_ylabel(uvot_rate)
ax3.set_ylabel(xrt_rate)
line3 = ax3.plot(y, label='XRT', color='gray')
vl = ax[0].axvline(0, ls='-', color='r', lw=1)    

ax[1].set_xlim(0,max(x))
ax[1].set_ylim(0,max(y))
ax[1].set_xlabel(uvot_rate)
ax[1].set_ylabel(xrt_rate)





def animate(i, vl):
    vl.set_xdata([i,i])
    sl = 30 # Show last n points
    if i < sl:
        line.set_data(x[:i], y[:i])  # update the data.
    if i >= sl:
        line.set_data(x[i-sl:i], y[i-sl:i])  # update the data.

    return line, vl

ani = animation.FuncAnimation(fig, animate, fargs=[vl], interval=80, blit=True, save_count=50)
plt.show()

