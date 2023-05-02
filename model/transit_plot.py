from area import Model
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R
import numpy as np
import matplotlib.colors as colors

if __name__ == "__main__":
    fig = plt.figure(figsize=(6,6), facecolor='white')
    ax1 = fig.add_subplot(111, projection='3d')


    ax1.set_title('3D')
    x0, y0, z0 = 0.0, 0.0, 20.0
    star_pos_init = np.array([x0, y0, z0])
 
    for phase_ang in np.arange(0,40,1):
        rot = R.from_euler('xyz', [0, phase_ang, 0], degrees=True)
        star_pos_rot = rot.apply(star_pos_init)
        

        mo_input = {'theta' : 5.0,
                    'x0' : star_pos_rot[0],
                    'y0' : star_pos_rot[1],
                    'z0' : star_pos_rot[2],
                    'r'  : 10.0,
                    'i'  : 0.0,
                    'mask_z':True}

        mo = Model(**mo_input)
        mo.run()
 

        ax1.plot(mo.x1, mo.y1, mo.z)
        ax1.plot(mo.x2, mo.y2, mo.z)




        extent = mo.extent

    # Plot inclination line y = mz
    #m = 1 / np.tan(np.deg2rad(mo.i)) # Gradient
    #xline = np.linspace(-10, 10, 10)
    #zline = m * xline
    #yline = np.zeros(10)
    #ax1.plot(xline, yline, zline, color='red', ls='dotted', label=f'i={mo.i}')
   
    ## Axes settings
    #ax1.set_xlabel('X')
    #ax1.set_ylabel('Y')
    #ax1.set_zlabel('Z')

    #ax1.view_init(elev=-28, azim=-108)

    #ax1.set_xticks([])
    #ax1.set_yticks([])
    #ax1.set_zticks([])
    
    
    # Set origin to center of star
    #pad = 1.5
    #ax1.set_xlim(mo.x0-pad*mo.r, mo.x0+pad*mo.r)
    #ax1.set_ylim(mo.y0-pad*mo.r, mo.y0+pad*mo.r)
    #ax1.set_zlim(mo.z0-pad*mo.r, mo.z0+pad*mo.r)
    ax1.set_box_aspect((1,1,1))
    
    ax1.legend()


    #ax1.set_axis_off()
    plt.show()


               

 
