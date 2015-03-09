import numpy as np
import cartesian
import rad_invdisttree

def regular_grid_data(array, x_spacing, y_spacing, base=10):
    '''
    Takes array of X, Y, Z data
    
    Grids to x_spacing and y_spacing
    
    X and y are set to allow Geoplot to deal with data
    '''
    from sklearn.neighbors import KDTree
    #from invdisttree import cartesian

    x_min, x_max = np.min(array[:,0]), np.max(array[:,0])
    y_min, y_max = np.min(array[:,1]), np.max(array[:,1])
    
    #rounds minimum values down to the nearest integer
    x_min, y_min = np.floor(x_min), np.floor(y_min)
    x_max, y_max = np.ceil(x_max), np.ceil(y_max)
    
    #Calculates number of points required in each direction
    x_range, y_range = x_max-x_min, y_max-y_min
    x_int, y_int = np.ceil((x_range/x_spacing)/base)*base, np.ceil((y_range/y_spacing)/base)*base
    
    #redefines max values based on multiples of base
    x_max, y_max = x_min + x_int*x_spacing + 0.5*x_spacing, y_min + y_int*y_spacing + 0.5 * y_spacing
    
    #moves x_min to midpoint of sample interval
    x_min, y_min = x_min + 0.5*x_spacing, y_min + 0.5*y_spacing
    
    #produces list of x points & y points
    x_val = np.arange(x_min,x_max, x_spacing)
    #print x_val
    #print
    y_val = np.arange(y_min,y_max, y_spacing)
    #print y_val
    #print y_min, y_max, x_spacing, y_spacing

    # calculate xy positions of each interpolation point
    xyi = cartesian(([x_val[None,:]],[y_val[:,None]]))
    
    #print xyi
    #Creates a tree of incoming points
    tree = KDTree(array[:,0:2])
    
    #interpolates to points
    za = rad_invdisttree(tree, xyi, array[:,2], np.mean((x_spacing,y_spacing)))

    #reshapes interpolated data
    xyzi = np.column_stack((xyi, za))
    
    i = np.lexsort((xyzi[:,0], xyzi[:,1]))
    xyzi = xyzi[i]

    x = np.reshape(xyzi[:,0], (len(y_val), len(x_val)))
    y = np.reshape(xyzi[:,1], (len(y_val), len(x_val)))
    z = np.reshape(xyzi[:,2], (len(y_val), len(x_val)))
    
    z[z==4095] = np.NaN
    z = np.ma.masked_array(z, np.isnan(z))
    
    header =str(x_min) + ' ' + str(x_max) + '\n' + str(y_min) + ' ' + str(y_max) + '\n' + str(np.min(z)) + ' ' + str(np.max(z)) + '\n' 
    
    val_dimens = (len(x_val), len(y_val))
    xbounds = (x_min, x_max-x_spacing)
    ybounds = (y_min, y_max-y_spacing)
    zbounds = (np.min(z), np.max(z))
    
    return x, y, z, val_dimens, xbounds,ybounds,zbounds