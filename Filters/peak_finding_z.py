# -*- coding: utf-8 -*-
"""
Created on Wed Dec 10 12:26:07 2014

@author: FPopecarter
"""

from shapely.geometry import mapping, Point
import fiona

import glob
import os

from osgeo import gdal
from osgeo import osr

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import scipy.ndimage as ndimage
import scipy.ndimage.filters as filters
from scipy import misc

from ArchaeoPY.Positional.points import Rotate2D
from ArchaeoPY.Filters.Analytical import ansig
from PIL import Image

def pixelToLatLon(World_addr,pixelPairs, cnt):
    
    lines = open(World_addr).readlines()
    x_s = float(lines[0])
    rot_x = float(lines[1])
    rot_y = float(lines[2])
    y_s = float(lines[3])
    UL_x = float(lines[4])
    UL_y = float(lines[5])
    
    print x_s, rot_x, rot_y, y_s, UL_x, UL_y
     
    pixelPairs = Rotate2D(pixelPairs,(0,0), np.deg2rad(-90))
    for point in pixelPairs:
        point[0],point[1] = (x_s*point[0])+(rot_x*point[1])+(UL_x),(rot_x*point[0])+(y_s*point[1])+UL_y
    return pixelPairs

 
os.chdir('C:/GeoSuB/Outputs')

dirs = glob.glob('*MEN*')

print dirs

for directory in dirs:
    print os.path.abspath(directory)
    os.chdir(directory)
    files = glob.glob('*Z.txt')
    print files
    for fname in files:
        
        ary = np.loadtxt(fname)
        ary = ary.reshape((120,160))
        ary = ndimage.zoom(ary, (2,1))
        imgplot = plt.imshow(ary, cmap = 'Greys', interpolation='none', vmin=np.percentile(ary,10), vmax=np.percentile(ary,90), aspect= 'equal', origin='upper')
        plt.show(block=False)
        plt.close()
        
        ary = ansig(ary, 0.25, 0.25)
        
        ##filtering parameters
        filter_size = [8,8]
        tharyhold = np.percentile(ary,95)
        
        cmap = cm.Greys
        cmap.set_bad('b',1.)  
        
        max_f = filters.maximum_filter(ary, size = filter_size)
        maxima = (ary == max_f)
        
        min_f = filters.minimum_filter(ary, size=filter_size)
        diff = ((max_f - min_f) > tharyhold)    
        maxima[diff == 0] = 0
        
        labeled, num_objects = ndimage.label(maxima)
        imgplot = plt.imshow(ary, cmap = 'jet',vmin=np.percentile(ary,10), vmax=np.percentile(ary,90), interpolation='none')
        
        out_fname = fname + '.any.png'
        out = np.subtract(np.copy(ary), np.percentile(np.isfinite(ary),10))
        out = np.divide(out,np.percentile(out[np.isfinite(out)], 90))
        out = np.flipud(out)
        im = Image.fromarray(np.uint8(cm.jet(out)*255))
        im.save(out_fname)
        
        
        xy = np.array(ndimage.center_of_mass(ary, labeled, range(1, num_objects+1)))
        #np.savetxt(fname + '.xy.csv', xy_out, delimiter=',', header='x,y', comments='')
        
        xy_out = np.divide(np.copy(xy),4.0)
        xy_out[:,0] = np.add(xy_out[:,0],0.25)
        #xy_out = np.divide(xy_out, 1.032)
        cnt = (417964.387,443383.616)
        rot_ang = np.deg2rad(32.16066)
        
        xy_out = Rotate2D(xy_out, (0,0), ang=rot_ang)
        xy_out = np.add(xy_out, cnt)
        
        schema = {
            'geometry': 'Point',
            'properties': {'id':'int'},
        }
        i = 0
        with fiona.open(fname + '.xy.shp', 'w', 'ESRI Shapefile', schema) as c:
            for row in xy_out:
                point = Point(row)
                c.write({
                'geometry':mapping(point),
                'properties': {'id':i},
                })
                i += 1
        
        plt.savefig('Points.png', bbox_inches = 'tight')
        plt.autoscale(False)
        plt.plot(xy[:, 1], xy[:, 0], 'ro')
        #plt.plot(5,5,'ro')
        #plt.plot(150,150,'bo')
        #plt.savefig('aryult.png', bbox_inches = 'tight')
        plt.show(block=False)
        plt.close()
        
    os.chdir('..')