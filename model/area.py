from time import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from sympy import symbols, Eq, solve, nsolve, latex
from sympy.utilities.lambdify import lambdify
from scipy.spatial.transform import Rotation as R
from skspatial.measurement import area_signed


np.seterr(invalid='ignore') # Ignore sqrt(nan)
np.set_printoptions(threshold=10, linewidth=150, precision=4)   #np.inf


def autosize_ax_sq(ax):
    """Automatically set the axes limits to roughly square."""
    xlow, xhigh = ax.get_xlim()
    ylow, yhigh = ax.get_ylim()

    ax_max = max(abs(np.array([xlow, ylow, xhigh, yhigh])))
    ax_max
    pad = 1.1

    ax.set_xlim(-pad*ax_max, pad*ax_max)
    ax.set_ylim(-pad*ax_max, pad*ax_max)
    
    
class Model:
    def __init__(self, theta, x0, y0, z0, r, i, mask_z):
        self.theta  = np.deg2rad(theta)
        self.x0     = x0
        self.y0     = y0
        self.z0     = z0
        self.r      = r
        self.i      = i
        self.mask_z = mask_z


        # Calculate the area  
        self.c = np.sin(self.theta/2) # Conic opening parameter (R/H)
        self.h_cone = 1 # Height of inner cone 
        self.r_cone = self.h_cone * np.tan(self.theta/2)
        self.A_cone = np.pi * self.r_cone**2
        self.A_cone_proj = self.A_cone * np.cos(self.i)

        self.extent = 20

        self.ngrid = 10000
        
        # Timers
        self.t_eval = np.nan
        self.t_plot = np.nan
        
        
        # Initialize segments
        self.x1_rot_seg1 = [np.nan]
        self.y1_rot_seg1 = [np.nan]
        self.x2_rot_seg1 = [np.nan]
        self.y2_rot_seg1 = [np.nan]
        
        self.x1_rot_seg2 = [np.nan]
        self.y1_rot_seg2 = [np.nan]
        self.x2_rot_seg2 = [np.nan]
        self.y2_rot_seg2 = [np.nan]
        
        
        # Initialize areas
        self.area_x1_y1_seg1 = np.nan
        self.area_x2_y2_seg1 = np.nan
        self.area_x1_y1_rot_seg1 = np.nan
        self.area_x2_y2_rot_seg1 = np.nan
        self.area_x1_y1_seg2 = np.nan
        self.area_x2_y2_seg2 = np.nan
        self.area_x1_y1_rot_seg2 = np.nan
        self.area_x2_y2_rot_seg2 = np.nan

    def __str__(self):
        return f'theta_{np.rad2deg(self.theta):.2f},x0_{self.x0},y0_{self.y0},z0_{self.z0},r_{self.r},i_{self.i},mask_z_{self.mask_z}'
        
    def __str_latex__(self):
        return fr'$\theta$ = {np.rad2deg(self.theta):.2f}$^\circ$ $x_0$ = {self.x0} $y_0$ = {self.y0} $z_0$ = {self.z0} $r$ = {self.r} $i$ = {self.i} mask_z = {self.mask_z}'

    def f_x1(self, z):
        c, x0, y0, z0, r = self.c, self.x0, self.y0, self.z0, self.r
        return (c**2*z**2 - r**2 + x0**2 + y0**2 - 2*y0*(-x0*np.sqrt(-c**4*z**4 + 2*c**2*r**2*z**2 + 2*c**2*x0**2*z**2 + 2*c**2*y0**2*z**2 - 2*c**2*z**4 + 4*c**2*z**3*z0 - 2*c**2*z**2*z0**2 - r**4 + 2*r**2*x0**2 + 2*r**2*y0**2 + 2*r**2*z**2 - 4*r**2*z*z0 + 2*r**2*z0**2 - x0**4 - 2*x0**2*y0**2 - 2*x0**2*z**2 + 4*x0**2*z*z0 - 2*x0**2*z0**2 - y0**4 - 2*y0**2*z**2 + 4*y0**2*z*z0 - 2*y0**2*z0**2 - z**4 + 4*z**3*z0 - 6*z**2*z0**2 + 4*z*z0**3 - z0**4)/(2*(x0**2 + y0**2)) + y0*(c**2*z**2 - r**2 + x0**2 + y0**2 + z**2 - 2*z*z0 + z0**2)/(2*(x0**2 + y0**2))) + z**2 - 2*z*z0 + z0**2)/(2*x0)
        
    def f_x2(self, z):
        c, x0, y0, z0, r = self.c, self.x0, self.y0, self.z0, self.r
        return (c**2*z**2 - r**2 + x0**2 + y0**2 - 2*y0*(x0*np.sqrt(-c**4*z**4 + 2*c**2*r**2*z**2 + 2*c**2*x0**2*z**2 + 2*c**2*y0**2*z**2 - 2*c**2*z**4 + 4*c**2*z**3*z0 - 2*c**2*z**2*z0**2 - r**4 + 2*r**2*x0**2 + 2*r**2*y0**2 + 2*r**2*z**2 - 4*r**2*z*z0 + 2*r**2*z0**2 - x0**4 - 2*x0**2*y0**2 - 2*x0**2*z**2 + 4*x0**2*z*z0 - 2*x0**2*z0**2 - y0**4 - 2*y0**2*z**2 + 4*y0**2*z*z0 - 2*y0**2*z0**2 - z**4 + 4*z**3*z0 - 6*z**2*z0**2 + 4*z*z0**3 - z0**4)/(2*(x0**2 + y0**2)) + y0*(c**2*z**2 - r**2 + x0**2 + y0**2 + z**2 - 2*z*z0 + z0**2)/(2*(x0**2 + y0**2))) + z**2 - 2*z*z0 + z0**2)/(2*x0)
        
       
    def f_y1(self, z):
        c, x0, y0, z0, r = self.c, self.x0, self.y0, self.z0, self.r
        return -x0*np.sqrt(-c**4*z**4 + 2*c**2*r**2*z**2 + 2*c**2*x0**2*z**2 + 2*c**2*y0**2*z**2 - 2*c**2*z**4 + 4*c**2*z**3*z0 - 2*c**2*z**2*z0**2 - r**4 + 2*r**2*x0**2 + 2*r**2*y0**2 + 2*r**2*z**2 - 4*r**2*z*z0 + 2*r**2*z0**2 - x0**4 - 2*x0**2*y0**2 - 2*x0**2*z**2 + 4*x0**2*z*z0 - 2*x0**2*z0**2 - y0**4 - 2*y0**2*z**2 + 4*y0**2*z*z0 - 2*y0**2*z0**2 - z**4 + 4*z**3*z0 - 6*z**2*z0**2 + 4*z*z0**3 - z0**4)/(2*(x0**2 + y0**2)) + y0*(c**2*z**2 - r**2 + x0**2 + y0**2 + z**2 - 2*z*z0 + z0**2)/(2*(x0**2 + y0**2))
        
        
    def f_y2(self, z):
        c, x0, y0, z0, r = self.c, self.x0, self.y0, self.z0, self.r
        return x0*np.sqrt(-c**4*z**4 + 2*c**2*r**2*z**2 + 2*c**2*x0**2*z**2 + 2*c**2*y0**2*z**2 - 2*c**2*z**4 + 4*c**2*z**3*z0 - 2*c**2*z**2*z0**2 - r**4 + 2*r**2*x0**2 + 2*r**2*y0**2 + 2*r**2*z**2 - 4*r**2*z*z0 + 2*r**2*z0**2 - x0**4 - 2*x0**2*y0**2 - 2*x0**2*z**2 + 4*x0**2*z*z0 - 2*x0**2*z0**2 - y0**4 - 2*y0**2*z**2 + 4*y0**2*z*z0 - 2*y0**2*z0**2 - z**4 + 4*z**3*z0 - 6*z**2*z0**2 + 4*z*z0**3 - z0**4)/(2*(x0**2 + y0**2)) + y0*(c**2*z**2 - r**2 + x0**2 + y0**2 + z**2 - 2*z*z0 + z0**2)/(2*(x0**2 + y0**2))
       

    def calc_equator_circle(self):
        """Calculate the points on a circle around the z axis of the star"""
        n = self.ngrid
        i = np.arange(0,n,1)
        self.x_circ = self.x0 + np.cos(2*np.pi / n * i) * self.r
        self.y_circ = self.y0 + np.sin(2*np.pi / n * i) * self.r
        self.z_circ = self.z0 + np.zeros(n)


    def area_2d(self, x, y):
        """Calculate area via Shoelace Method."""
        if len(x) < 3 or len(y) < 3:
            print('Length of segment is < 3 area = 0')
            return 0
        return area_signed(np.column_stack([x, y]))
        
    def plot_3d(self):
        """ Just plot the 3d bit"""
        fig = plt.figure(figsize=(3.5,3.5))
        ax1 = fig.add_subplot(111, projection='3d')
# Calculate cone & grid
        extent = self.extent
        c = self.c
        r = self.r
        x0, y0, z0 = self.x0, self.y0, self.z0
        
        xs = np.linspace(-extent, extent, 1000)
        ys = np.linspace(-extent, extent, 1000)
        X, Y = np.meshgrid(xs,ys)
        Z = np.sqrt((X**2 + Y**2)/c**2)

        # Calculate z limits
        z = np.linspace(-extent, extent, self.ngrid)

        #plt.suptitle(f'{self.__str_latex__()}')
        
        #ax1.set_title('3D')
        # plot cone
        # surf = ax1.plot_surface(X,Y,Z, alpha=0.5, color='cyan')
        
        # Plot intersection lines
        ax1.plot(self.x1, self.y1, self.z, color='red')
        ax1.plot(self.x2, self.y2, self.z, color='black')
        ax1.set_zlim(-extent, extent)
        
        # Plot Sphere
        u, v = np.mgrid[0:2*np.pi:30j, 0:np.pi:20j]
        x_sp = x0 + r*np.cos(u)*np.sin(v)
        y_sp = y0 + r*np.sin(u)*np.sin(v)
        z_sp = z0 + r*np.cos(v)
        #ax1.plot_wireframe(x_sp, y_sp, z_sp, color="grey", alpha=0.5)
        ax1.plot_surface(x_sp, y_sp, z_sp, color="lightblue", alpha=0.5)
        #plot_surface

        """
        # Plot inclination line y = mz
        m = 1 / np.tan(np.deg2rad(self.i)) # Gradient
        xline = np.linspace(-10, 10, 10)
        zline = m * xline
        yline = np.zeros(10)
        ax1.plot(xline, yline, zline, color='red', ls='dotted', label=f'i={self.i}')
        """
        
        # Axes settings
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        ax1.set_zlabel('Z')
        
        ax1.view_init(elev=10, azim=-152)

        ax1.set_xticks([])
        ax1.set_yticks([])
        ax1.set_zticks([])
        
        
        # Set origin to center of star
        pad = 1.5
        ax1.set_xlim(self.x0-pad*self.r, self.x0+pad*self.r)
        ax1.set_ylim(self.y0-pad*self.r, self.y0+pad*self.r)
        ax1.set_zlim(self.z0-pad*self.r, self.z0+pad*self.r)
        ax1.set_box_aspect((1,1,1))
        plt.savefig('../figures/3d_intersection.png', bbox_inches='tight')
        plt.savefig('../figures/3d_intersection.pdf', bbox_inches='tight')

    def plot(self):
        t0 = time()
        
        fig = plt.figure(figsize=(15,7.5))
        ax1 = fig.add_subplot(121, projection='3d')
        ax2 = fig.add_subplot(243)
        ax3 = fig.add_subplot(244)
        ax4 = fig.add_subplot(247)
        ax5 = fig.add_subplot(248)

        # Calculate cone & grid
        extent = self.extent
        c = self.c
        r = self.r
        x0, y0, z0 = self.x0, self.y0, self.z0
        
        xs = np.linspace(-extent, extent,100)
        ys = np.linspace(-extent, extent,100)
        X, Y = np.meshgrid(xs,ys)
        Z = np.sqrt((X**2 + Y**2)/c**2)

        # Calculate z limits
        z = np.linspace(-extent, extent, self.ngrid)

        plt.suptitle(f'{self.__str_latex__()}')
        
        ax1.set_title('3D')
        # plot cone
        # surf = ax1.plot_surface(X,Y,Z, alpha=0.5, color='cyan')
        
        # Plot intersection lines
        ax1.plot(self.x1, self.y1, self.z, color='red')
        ax1.plot(self.x2, self.y2, self.z, color='black')
        ax1.set_zlim(-extent, extent)
        
        # Plot Sphere
        u, v = np.mgrid[0:2*np.pi:30j, 0:np.pi:20j]
        x_sp = x0 + r*np.cos(u)*np.sin(v)
        y_sp = y0 + r*np.sin(u)*np.sin(v)
        z_sp = z0 + r*np.cos(v)
        ax1.plot_wireframe(x_sp, y_sp, z_sp, color="grey", alpha=0.8)

        # Plot equatorial circle
        ax1.plot(self.x_circ, self.y_circ, self.z_circ, color='blue')


        # Plot inclination line y = mz
        m = 1 / np.tan(np.deg2rad(self.i)) # Gradient
        xline = np.linspace(-10, 10, 10)
        zline = m * xline
        yline = np.zeros(10)
        ax1.plot(xline, yline, zline, color='red', ls='dotted', label=f'i={self.i}')
       
        # Axes settings
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        ax1.set_zlabel('Z')

        ax1.view_init(elev=-28, azim=-108)

        #ax1.set_xticks([])
        #ax1.set_yticks([])
        #ax1.set_zticks([])
        
        
        # Set origin to center of star
        pad = 1.5
        ax1.set_xlim(self.x0-pad*self.r, self.x0+pad*self.r)
        ax1.set_ylim(self.y0-pad*self.r, self.y0+pad*self.r)
        ax1.set_zlim(self.z0-pad*self.r, self.z0+pad*self.r)
        ax1.set_box_aspect((1,1,1))
        
        ax1.legend()
        
        # Plot x, y plane (TOP)
        ax2.set_title('TOP')
        ax2.plot(self.x1, self.y1, color='red', label='x1,y1')
        ax2.plot(self.x2, self.y2, color='black', label='x2,y2')
        ax2.set_xlabel('x')
        ax2.set_ylabel('y')

        # Plot equatorial circle
        ax2.plot(self.x_circ, self.y_circ, color='blue')

        # plot maximum & minimum x and y
        ax2.scatter(self.x1[0], self.y1[0], label='x1,y1[0]')
        ax2.scatter(self.x1[-1], self.y1[-1], label='x1,y1[-1]')
        ax2.scatter(self.x2[0], self.y2[0], label='x2,y2[0]')
        ax2.scatter(self.x2[-1], self.y2[-1], label='x2,y2[-1]')

        ax2.legend()
        autosize_ax_sq(ax2)

        # Plot x, z plane (SIDE)
        ax3.set_title('SIDE (X,Z)')
        ax3.plot(self.x1, self.z, color='red', label='x1,z1')
        ax3.plot(self.x2, self.z, color='black', label='x2,z2')
        
        # Plot equatorial circle
        ax3.plot(self.x_circ, self.z_circ, color='blue')

        ax3.set_xlabel('x')
        ax3.set_ylabel('z')
        ax3.legend()
        autosize_ax_sq(ax3)

        # Plot y, z plane (SIDE)
        ax4.set_title('SIDE (Y,Z)')
        ax4.plot(self.y1, self.z, color='red', label='y1,z1')
        ax4.plot(self.y2, self.z, color='black', label='y2,z1')

        # Plot equatorial circle
        ax4.plot(self.y_circ, self.z_circ, color='blue')


        ax4.set_xlabel('y')
        ax4.set_ylabel('z')
        ax4.legend()
        autosize_ax_sq(ax4)
        
        # Plot projected plane at specific inclination
        ax5.set_title(f'PROJ i = {self.i}')
        ax5.plot(self.x1_rot_seg1, self.y1_rot_seg1, color='red', label=f'x1_y1_rot_seg1 A={self.area_x1_y1_rot_seg1:.2f}')#, label=f'A = {self.area_x1_y1_rot_seg1:.2f}')
        ax5.plot(self.x2_rot_seg1, self.y2_rot_seg1, color='black', label=f'x2_y2_rot_seg1 A={self.area_x2_y2_rot_seg1:.2f}')#, label=f'A = {self.area_x2_y2_rot_seg2:.2f}')
        ax5.plot(self.x1_rot_seg2, self.y1_rot_seg2, color='darkred', label=f'x1_y1_rot_seg2 A={self.area_x1_y1_rot_seg2:.2f}')#, label=f'A = {self.area_x1_y1_rot_seg1:.2f}')
        ax5.plot(self.x2_rot_seg2, self.y2_rot_seg2, color='grey', label=f'x2_y2_rot_seg2 A={self.area_x2_y2_rot_seg2:.2f}')#, label=f'A = {self.area_x2_y2_rot_seg2:.2f}')

        # A rotated sphere is still a sphere, a rotated circle however is not...
        ax5.plot(self.x_circ, self.y_circ, color='lightblue')

        # plot maximum & minimum x and y
        ax5.scatter(self.x1_rot_seg1[-1], self.y1_rot_seg1[-1], label='x1,y1_rot_seg1[-1]')
        ax5.scatter(self.x2_rot_seg1[-1], self.y2_rot_seg1[-1], label='x1,y1_rot_seg1[-1]')

        # ax5.scatter(self.x1_rot_seg2[-1], self.y1_rot_seg2[-1], label='x1,y1_rot_seg2[-1]')


 


        ax5.set_xlabel('x')
        ax5.set_ylabel('y')
        ax5.legend(fontsize=7)
        autosize_ax_sq(ax5)
        
        
        #plt.tight_layout()
        
        #fn = f'plt_out/{self.__str__()}.png'
        #print(f'Saving to : {fn}')
        #plt.savefig(fn)
        self.t_plot = time() - t0
        # plt.show()
        
        # plt.close(fig)
        
        
    def run(self):
        t0 = time()
        
        self.z = np.linspace(-self.extent, self.extent, 10000)
        
        # Limit z values to lower hemisphere of the sphere
        if self.mask_z:
            mask = np.where(self.z < self.z0)
            self.z = self.z[mask]
        
        # Calculate the circle around the equator of the star
        self.calc_equator_circle()

        # Calculate the intersections
        self.x1 = self.f_x1(self.z)
        self.x2 = self.f_x2(self.z)
        self.y1 = self.f_y1(self.z)
        self.y2 = self.f_y2(self.z)
        
        # Reshape coordinates
        vecs1 = np.vstack([self.x1, self.y1, self.z]).T # [[x1,y1,z1],[x1,y2,z2],...[xn,yn,zn]]
        vecs2 = np.vstack([self.x2, self.y2, self.z]).T
        vecs_circ = np.vstack([self.x_circ, self.y_circ, self.z_circ]).T
        
        # Create Rotation Vector
        rot = R.from_euler('zyx', [0, self.i, 0], degrees=True)
        
        # Apply rotation Vector
        vecs_rotated1 = rot.apply(vecs1)
        vecs_rotated2 = rot.apply(vecs2)

        vecs_circ_rotated = rot.apply(vecs_circ)
        
        # Reshape Coordinates
        self.x1_rot, self.y1_rot, self.z1_rot = vecs_rotated1.T
        self.x2_rot, self.y2_rot, self.z2_rot = vecs_rotated2.T
        self.x_circ_rot, self.y_circ_rot, self.z_circ_rot = vecs_circ_rotated.T

        
        # Find the continuous line segments that where successfully evaluated for a given z
        # x1 = [nan,nan,nan]                                     idx = []
        # x1 = [nan,nan,1,2,4,nan]                               idx = [2,5]
        # x1 = [nan,nan,nan,nan,3,2,3,4,na,nan,nan]              idx = [4,8]
        # x1 = [nan,nan,nan,2,4,5,nan,nan,nan,3,4,5,nan,nan]     idx = [3,6,10,13]
        # x1 = [nan,nan,nan,3,4,5]                               idx = [3] <-- This may need larger z range?
        #
        
        idxs_x = np.where(np.diff(np.isnan(self.x1_rot)))[0] # indexs where the two parts of the curve start and end.
        idxs_y = np.where(np.diff(np.isnan(self.y1_rot)))[0] # indexs where the two parts of the curve start and end.
       
        self.idx = idxs_x


        if len(idxs_x) == 0:
            print('No segments found, star outside the cone?')
            return 1
        
        if len(idxs_x) == 1:
            print('WARNING! len(idxs_x) == 1 curve may be outside of zrange...')
            self.x1_seg1 = self.x1[idxs_x[0]+1:]
            self.y1_seg1 = self.y1[idxs_x[0]+1:]
            self.x2_seg1 = self.x1[idxs_x[0]+1:]
            self.y2_seg1 = self.y2[idxs_x[0]+1:]
            
            self.x1_rot_seg1 = self.x1[idxs_x[0]+1:]
            self.y1_rot_seg1 = self.y1[idxs_x[0]+1:]
            self.x2_rot_seg1 = self.x2[idxs_x[0]+1:]
            self.y2_rot_seg1 = self.y2[idxs_x[0]+1:]
        
        if len(idxs_x) == 2:
            # One segment (grazing)
            print('one segment, grazing?')
            self.x1_seg1 = self.x1[idxs_x[0]+1:idxs_x[1]]
            self.y1_seg1 = self.y1[idxs_x[0]+1:idxs_x[1]]
            self.x2_seg1 = self.x2[idxs_x[0]+1:idxs_x[1]]
            self.y2_seg1 = self.y2[idxs_x[0]+1:idxs_x[1]]
            
            self.x1_rot_seg1 = self.x1_rot[idxs_x[0]+1:idxs_x[1]]
            self.y1_rot_seg1 = self.y1_rot[idxs_y[0]+1:idxs_y[1]]
            self.x2_rot_seg1 = self.x2_rot[idxs_x[0]+1:idxs_x[1]]
            self.y2_rot_seg1 = self.y2_rot[idxs_y[0]+1:idxs_y[1]]

        if len(idxs_x) == 4:
            # Two segments (full crossing)
            self.x1_seg1 = self.x1[idxs_x[0]+1:idxs_x[1]]
            self.x1_seg2 = self.x1[idxs_x[2]+1:idxs_x[3]]

            self.y1_seg1 = self.y1[idxs_y[0]+1:idxs_y[1]]
            self.y1_seg2 = self.y1[idxs_y[2]+1:idxs_y[3]]

            self.x2_seg1 = self.x2[idxs_x[0]+1:idxs_x[1]]
            self.x2_seg2 = self.x2[idxs_x[2]+1:idxs_x[3]]

            self.y2_seg1 = self.y2[idxs_y[0]+1:idxs_y[1]]
            self.y2_seg2 = self.y2[idxs_y[2]+1:idxs_y[3]]

            self.x1_rot_seg1 = self.x1_rot[idxs_x[0]+1:idxs_x[1]]
            self.x1_rot_seg2 = self.x1_rot[idxs_x[2]+1:idxs_x[3]]

            self.y1_rot_seg1 = self.y1_rot[idxs_y[0]+1:idxs_y[1]]
            self.y1_rot_seg2 = self.y1_rot[idxs_y[2]+1:idxs_y[3]]

            self.x2_rot_seg1 = self.x2_rot[idxs_x[0]+1:idxs_x[1]]
            self.x2_rot_seg2 = self.x2_rot[idxs_x[2]+1:idxs_x[3]]

            self.y2_rot_seg1 = self.y2_rot[idxs_y[0]+1:idxs_y[1]]
            self.y2_rot_seg2 = self.y2_rot[idxs_y[2]+1:idxs_y[3]]

        
        # Calculate areas
        if len(idxs_x) >= 2:
            self.area_x1_y1_seg1 = self.area_2d(self.x1_seg1, self.y1_seg1)
            self.area_x2_y2_seg1 = self.area_2d(self.x2_seg1, self.y2_seg1)

            self.area_x1_y1_rot_seg1 = self.area_2d(self.x1_rot_seg1, self.y1_rot_seg1)
            self.area_x2_y2_rot_seg1 = self.area_2d(self.x2_rot_seg1, self.y2_rot_seg1)
            
        if len(idxs_x) == 4:
            self.area_x1_y1_seg2 = self.area_2d(self.x1_seg2, self.y1_seg2)
            self.area_x2_y2_seg2 = self.area_2d(self.x2_seg2, self.y2_seg2)
            
            self.area_x1_y1_rot_seg2 = self.area_2d(self.x1_rot_seg2, self.y1_rot_seg2)
            self.area_x2_y2_rot_seg2 = self.area_2d(self.x2_rot_seg2, self.y2_rot_seg2)
        
        self.t_eval = time() - t0
        return 0

    def print(self):
        for k, v in self.__dict__.items():
            print(f'{str(type(v)):<25} {k:<20} : {v}')
    
    def collect(self):
        d = {}
        for k, v in self.__dict__.items():
            if isinstance(v, (int, float, bool, np.int64, np.float64)):
                d[k] = v
        return d


if __name__ == "__main__":
    x0, y0, z0 = 0.0, 0.0, 10.0
    star_pos_init = np.array([x0, y0, z0])
    
    res = []
    
    for phase_ang in np.arange(0,5,0.1):
        rot = R.from_euler('xyz', [0, phase_ang, 0], degrees=True)
        star_pos_rot = rot.apply(star_pos_init)
        
        mo_input = {'theta' : 15.0,
                    'x0' : star_pos_rot[0],
                    'y0' : star_pos_rot[1],
                    'z0' : star_pos_rot[2],
                    'r'  : 2.2,
                    'i'  : 7.4,
                    'mask_z':False}
                    

        mo = Model(**mo_input)
        mo.run()
        mo.plot()
        mo.print()
        out = mo.collect()
        out['phase_ang'] = phase_ang
        res.append(out)
        
    df_res = pd.DataFrame(res)
    
    
    # Calculate secondary quantities
    df_res['area_seg1']   = df_res['area_x1_y1_seg1'].abs() + df_res['area_x2_y2_seg1'].abs()
    df_res['area_seg2']   = df_res['area_x1_y1_seg2'].abs() + df_res['area_x2_y2_seg2'].abs()
    
    df_res['area_seg1_rot']   = df_res['area_x1_y1_rot_seg1'].abs() + df_res['area_x2_y2_rot_seg1'].abs()
    df_res['area_seg2_rot']   = df_res['area_x2_y2_rot_seg2'].abs() + df_res['area_x2_y2_rot_seg2'].abs()
    
    df_res['area_star_2d'] = np.pi * df_res['r']**2
    
    df_res['area_ratio_seg1_star'] = df_res['area_seg1'] / df_res['area_star_2d']
    df_res['area_ratio_seg2_star'] = df_res['area_seg2'] / df_res['area_star_2d']
    
    df_res['area_ratio_seg1_rot_star'] = df_res['area_seg1_rot'] / df_res['area_star_2d']
    df_res['area_ratio_seg2_rot_star'] = df_res['area_seg2_rot'] / df_res['area_star_2d']
    
    
    
    
    
    
    plt.plot(df_res['phase_ang'], df_res['area_ratio_seg1_rot_star'], label='Projected area seg1')
    plt.plot(df_res['phase_ang'], df_res['area_ratio_seg2_rot_star'], label='Projected area seg2')
    plt.xlabel('Orbital Phase angle')
    plt.ylabel(r'Irradiated Fraction (A / $\pi r^2$)')
    
    plt.legend()
    plt.show()
    
    
