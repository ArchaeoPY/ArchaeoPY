# -*- coding: utf-8 -*-
"""
ArchaeoPY.IO.geoplot

Load_Comp(fname,grid_length,grid_width,sample_interval,traverse_interval)

Returns np array of shape grid_width / traverse_interval by grid_length / sample_interval
"""
import numpy as np
import sys

def Load_Comp(fname,grid_length,grid_width,sample_interval,traverse_interval):
    """
    fname; File path of Geoplot .cmp file
    grid_length; length of grid (traverse) in m
    grid_width; width of grid (m) (traverse_interval * no. traverses)
    sample_interval; distance between in line samples (m)
    traverse_interval; distance between adjacent traverses
    
    Loads Geoplot .cmp files and returns an array of shape no.samples x no. traverses
    
    ##TODO Integrate .cmd header information to obtain comp size
    
    """
    
    #Opens & loads bytewise the cmp file into numpy array
    f = open(fname, 'rb')
    comp_array = np.fromfile(f, dtype='f')
    f.close()
    print np.shape(comp_array)
    
    #calculates desired shape & reshapes loaded data
    shape = (int(grid_width / traverse_interval),int(grid_length / sample_interval))    
    comp_array = comp_array.reshape(shape)
    
    #replaces geooplot dummy values with Nan
    comp_array[comp_array==2047.5] = np.nan
    
    #define min and max values
    M = "Min, Max and Mean:"
    print M
    print np.nanmin(comp_array), np.nanmax(comp_array), np.nanmean(comp_array)


    print np.nan
    #Returns modified array
    return comp_array

def Load_Geoplot_CMD(cmdname):
    """
    accepts:    
    cmdname; File path of Geoplot .cmp file with extension edited to cmd
    
    returns:
    grid_length; length of grid (traverse) in m
    grid_width; width of grid (m) (traverse_interval * no. traverses)
    sample_interval; distance between in line samples (m)
    traverse_interval; distance between adjacent traverses
    
    Loads Geoplot .cmd files and returns array dimensions
        
    """
    f = open(cmdname, 'r')
    lines = f.readlines()
    f.close()
    #From Note++ Defined which line to read. array so first is 0
    grid_length = float(lines[5][1:-4]) #Traverse Length
    grid_width = float(lines[6][1:-4]) #Width
    sample_interval = float(lines[8][1:-4])
    traverse_interval = float(lines[7][1:-4])
    print grid_length,grid_width,sample_interval,traverse_interval
    
    return grid_length,grid_width,sample_interval,traverse_interval
