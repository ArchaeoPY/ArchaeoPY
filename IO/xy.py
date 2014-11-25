"""
Comp to Dxf

Opens Geoplot Comp & allows to save as DXF

"""
import numpy as np
from dxfwrite import DXFEngine as dxf

def using_clump(x,y):
    '''
    x; 1-D array of x values
    y; 1-D array of y values
    
    splits data on nan in y
    
    Example:
    a = [10,11,12,13,14,15,16,17,18,19]
    b = [0,1,2,3,4,np.nan,6,7,8,9]
    
    Returns
    
    [
    array([[10,  0],
       [11,  1],
       [12,  2],
       [13,  3],
       [14,  4]]), 
       
       array([[16,  6],
       [17,  7],
       [18,  8],
       [19,  9]])]
    
    from http://stackoverflow.com/questions/14605734/numpy-split-1d-array-of-chunks-separated-by-nans-into-a-list-of-the-chunks
    '''
    #
    return [np.vstack((x[s],y[s])).T for s in np.ma.clump_unmasked(np.ma.masked_invalid(y))]
    
    
def comp2dxf(comp, fname, sample_interval, traverse_interval, scale, clip, layer):
    
    """
    comp; Numpy array of shape length, width
    fname; filepath to save dxf
    sample_interval; distance between samples (m)
    traverse_interval; distance between traverses
    scale; z units/cm
    clip; value to clip data at (z units)
    layer; name of dxf layer (string)
    """
    
    #Copies Comp & Flips along horizontal axis
    #Copy to avoid flipping,clipping original data
    #FlipUD due to positional referencing
    comp = np.flipud(np.copy(comp))
    
    #Initiates the dxf using DXFEngine
    drawing = dxf.drawing(fname)
    
    #Creates a layer for the polylines to reside
    drawing.add_layer(str(layer))
    
    #sets the first line position to be the centre of a traverse
    y = 0.5*traverse_interval

    #iterates through the traverses
    for row in comp:
        #Calculates the x position of each data point
        x_pos = np.arange(len(row))
        x_pos = np.multiply(x_pos,sample_interval)
        
        #clips the magnitude according to user input
        y_pos = np.clip(row,-clip,clip)
        
        #scales the magnitude according to user input
        y_pos = np.divide(np.multiply(y_pos,scale),clip*100)
        
        #shifts the magnitude to centre on correct traverse location
        y_pos = np.add(y_pos, y)
        
        #calculates position of next traverse
        y += traverse_interval
        
        #splits traverses on Nan. Polylines cannot bridge Nan
        lines = using_clump(x_pos, y_pos)
        
        #For each traverse section (from nan splitting) creates a polyline & adds to drawing
        for line in lines:
            polyline = dxf.polyline(layer=str(layer))
            polyline.add_vertices(line)
            drawing.add(polyline)
    
    #Saves Drawing
    drawing.save()
            

