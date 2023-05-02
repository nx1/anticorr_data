import numpy as np
from scipy.spatial import Delaunay

def area_triangulation(x, y):
    """
    Calculates the area of a shape defined by x-y coordinates using triangulation.
    
    Parameters:
    x (numpy array): x-coordinates of the shape
    y (numpy array): y-coordinates of the shape
    
    Returns:
    float: area of the shape
    """
    # stack the x and y coordinates into a single array
    coords = np.column_stack((x, y))
    
    # triangulate the coordinates
    try:
        tri = Delaunay(coords)
    except ValueError:
        print("Value Error, array probably contains NaNs, returning 0")
        return 0
    
    # calculate the area of each triangle
    areas = []
    for i in range(tri.simplices.shape[0]):
        # get the indices of the triangle vertices
        ia, ib, ic = tri.simplices[i, :]
        
        # get the coordinates of the triangle vertices
        a = coords[ia]
        b = coords[ib]
        c = coords[ic]
        
        # calculate the area of the triangle
        area = 0.5 * np.abs(a[0]*(b[1] - c[1]) + b[0]*(c[1] - a[1]) + c[0]*(a[1] - b[1]))
        areas.append(area)
    
    # return the total area
    return sum(areas)
