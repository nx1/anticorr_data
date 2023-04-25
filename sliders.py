import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

def get_ax_rect(ax):
    """Return [xmin,ymin,dx,dy]"""
    return ax.get_position().extents



parameters = ['par1','par2', 'par3', 'par4']

fig, ax = plt.subplots(figsize=(10,8))
rect = get_ax_rect(ax)

# Make room at bottom of figure for sliders
fig.subplots_adjust(bottom=0.25)

for i, p in enumerate(parameters):
    xmin = rect[0]
    ymin = rect[1] - i * 0.1
    dx = rect[2]
    dy = 0.03
    rect = [xmin, ymin, dx, dy]
    ax_slider = fig.add_axes(rect)

plt.show()



