import numpy as np
import matplotlib.pyplot as plt
from area import Model


m = Model(theta=15, x0=2.0, y0=0.0, z0=10.0, r=2.2, i=7.4, mask_z=False)
m2 = Model(theta=15, x0=2.0, y0=0.0, z0=10.0, r=2.2, i=7.4, mask_z=True)
m3 = Model(theta=15, x0=0.1, y0=0.0, z0=10.0, r=2.2, i=10.0, mask_z=True)

models = [m, m2, m3]


if __name__ == "__main__":

    
    for m in models:
        print('='*50)
        m.run()
        m.print()
        m.plot()
        m.plot_3d()

        x_seg1 = np.concatenate([m.x1_seg1, np.flip(m.x2_seg1)])
        y_seg1 = np.concatenate([m.y1_seg1, np.flip(m.y2_seg1)])
        
        x_rot_seg1 = np.concatenate([m.x1_rot_seg1, np.flip(m.x2_rot_seg1)])
        y_rot_seg1 = np.concatenate([m.y1_rot_seg1, np.flip(m.y2_rot_seg1)])
        
        A = m.area_2d(x_seg1, y_seg1)
        A_rot = m.area_2d(x_rot_seg1, y_rot_seg1)
        
        fig, ax = plt.subplots(figsize=(6,6))
        ax.plot(x_seg1, y_seg1, label=f'A={A:.2f} | x, y | mask_z={m.mask_z}')
        ax.plot(x_rot_seg1, y_rot_seg1, label=f'A={A_rot:.2f} | x,y rotated| mask_z={m.mask_z}')
        
        ax.legend()
        ax.set_xlim(-4,4)
        ax.set_ylim(-4,4)
        #input()
        break
    plt.show()


