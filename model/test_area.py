import numpy as np
import matplotlib.pyplot as plt
from area import Model


m = Model(theta=15, x0=2.0, y0=0.0, z0=10.0, r=2.2, i=7.4, mask_z=False)  # Grazing
m2 = Model(theta=15, x0=2.0, y0=0.0, z0=10.0, r=2.2, i=15.0, mask_z=True)  # Grazing
m3 = Model(theta=15, x0=0.1, y0=0.0, z0=10.0, r=2.2, i=10.0, mask_z=True) # Full intersection
m4 = Model(theta=15, x0=0.1, y0=0.0, z0=10.0, r=0.2, i=12, mask_z=True)    # Inside Cone
m5 = Model(theta=15, x0=15, y0=15, z0=3, r=1.0, i =10, mask_z=True)       # Outside cone

models = [m, m2, m3, m4, m5]


if __name__ == "__main__":
    
    for m in models:
        print('='*90)
        print(m)
        m.run()
        m.print()
        m.plot()
        #m.plot_3d()

        plt.show()


