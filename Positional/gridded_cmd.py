'''
Converts CMD data formats to surfer ASCII grids and tab separated spreadsheets

'''
import numpy as np
import glob
import matplotlib.pyplot as plt

def rad_invdisttree(tree, xy, z, radius):
    print radius
    groups, distances = tree.query_radius(xy, radius, return_distance=True)
    #groups2, distances2 = tree.query_radius(xy, radius*4, return_distance=True)

    interpol = np.zeros( (len(distances),) + np.shape(z[0]))
    interpol[interpol==0] = 4095

    jinterpol = 0
    i = 0
    for dist, ix in zip( distances, groups ):
        #print dist, ix
        if len(ix) == 0:
        #    if len(groups2[i]) == 0:
            wz = 4095
        #    else:
        #        w = 1 / distances2[i]**3
        #        w /= np.sum(w)
        #        wz = np.dot( w, z[groups2[i]])
        else:  # weight z s by 1/dist --
            w = 1 / dist**2
            w /= np.sum(w)
            wz = np.dot( w, z[ix])
        i +=1
        if np.isnan(wz):
            wz = 4095
        interpol[jinterpol] = wz
        jinterpol += 1
    return interpol

def surfer_txt_grid(filename, array, val_dimens, xbounds, ybounds, zbounds):

    array[np.isnan(array)] = float(1.70141e38)
    
    gridfile = open(filename, 'w')
    print >> gridfile, 'DSAA'
    print >> gridfile, str(val_dimens[0]) + ' ' + str(val_dimens[1])
    print >> gridfile, str(xbounds[0]) + ' ' + str(xbounds[1])
    print >> gridfile, str(ybounds[0]) + ' ' + str(ybounds[1])
    print >> gridfile, str(zbounds[0]) + ' ' + str(zbounds[1])
    print >> gridfile
    
    for row in array:
        #temp = list(row)
        #temp = ' '.join(temp)
        temp = ''
        delimiter = ' '
        #for item in row:
        print >> gridfile, delimiter.join(["%.5e" % (v) for v in row])
        print >> gridfile
    gridfile.close()
        
def geoplot_spreadsheet(filename, array, val_dimens, xbounds, ybounds, zbounds):

    array[array==1.70141e38] = float(2047.5)
    
    gridfile = open(filename, 'w')
#    print >> gridfile, 'DSAA'
#    print >> gridfile, str(val_dimens[0]) + ' ' + str(val_dimens[1])
#    print >> gridfile, str(xbounds[0]) + ' ' + str(xbounds[1])
#    print >> gridfile, str(ybounds[0]) + ' ' + str(ybounds[1])
#    print >> gridfile, str(zbounds[0]) + ' ' + str(zbounds[1])
#    print >> gridfile
    
    for row in array:
        #temp = list(row)
        #temp = ' '.join(temp)
        temp = ''
        delimiter = '	'
        #for item in row:
        print >> gridfile, delimiter.join(["%.3f" % (v) for v in row])
        #print >> gridfile
    gridfile.close()
    
def regular_grid_data(array, x_spacing, y_spacing, base=10):
    '''
    Takes array of X, Y, Z data
    
    Grids to x_spacing and y_spacing
    
    X and y are set to allow Geoplot to deal with data
    '''
    from sklearn.neighbors import KDTree
    from invdisttree import cartesian

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
    
    return x, y, z, val_dimens, xbounds,ybounds,zbounds, 

#define job name
job = 'men14_fixed'

#Plot images? True or False
plot = True

#makes a list of all files matching job
files = glob.glob(str(job) + '*'+'.txt')

#for this example we'll take the first file
filename = files[0]

#generates an array(spreadsheet) from the CMD data file. 
#Skips the first row because its a header
raw_array = np.loadtxt(filename, dtype=str, delimiter = '	', skiprows=1)

print raw_array
#determines number of datasets from shape of array
no_datasets = np.shape(raw_array)[1] -1

#Interpolates data to a grid useable by Geoplot

#define spacing of gridded data
x_spacing = 0.25
y_spacing = 1.0

#iterates over datasets - starts at 2 because no need to iterate over x & y positions
for i in range(2, no_datasets):
    #creates array from individual datasets
    array = np.column_stack((np.fliplr(raw_array[:,0:2]), raw_array[:, i])).astype(float)
    x, y, z, val_dimens, xbounds,ybounds,zbounds = regular_grid_data(array, x_spacing, y_spacing, base=10)
    fname = str(i) + str(job) + '.grd'
    surfer_txt_grid(fname, z, val_dimens, xbounds, ybounds, zbounds)
    fname = str(i) + str(job) + '.txt'
    geoplot_spreadsheet(fname, z, val_dimens, xbounds, ybounds, zbounds)
    
    if plot == True:
        z[z==2047.5] = np.nan
        im = plt.imshow(z,origin='lower', cmap=plt.cm.Greys, 
                        extent=(xbounds[0],xbounds[1],ybounds[0],ybounds[1]))
        plt.colorbar()
        plt.show()