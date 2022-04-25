import sys
from glob import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LogNorm
import astropy
from astropy.io import fits
from tqdm import tqdm

def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


def read_hdul(path):
    hdul = fits.open(path)
    
    print(hdul)
    return hdul

class Image:
    def __init__(self, data):
        self.data = data
        self.size = self.data.size

    def __repr__(self):
        return repr('Image')

    @classmethod
    def from_path(cls, path):
        hdul = fits.open(path)
        for i, h in enumerate(hdul):
            if type(h) is astropy.io.fits.hdu.image.ImageHDU:
                img = h.data
                t = i
        print(f'{path:<80} {img.shape} {img.size} {sizeof_fmt(sys.getsizeof(img))} t={t}')
        c = cls(img)
        c.path = path
        return c

    def plot(self):
       plt.figure()
       plt.imshow(self.data)
       plt.show()



img_files = glob('download_scripts/NGC1313/*/*u_sk.img.gz')

img_file = img_files[0]
img = Image.from_path(img_file)


images =  []

for path in img_files[:10]:
    try:
        image = Image.from_path(path)
        images.append(image)
    except UnboundLocalError:
        print(f'No image hdul found for {path}')


def animate(i):
    image = images[i]
    im.set_array(image.data)
    ax.set_title(image.path.split('/')[-1])
    return [im]

fig, ax = plt.subplots(1,1)
im = ax.imshow(images[0].data, norm=LogNorm(), cmap='hot')

ani = animation.FuncAnimation(fig, animate, interval=100, blit=False, frames=10)
plt.show()


