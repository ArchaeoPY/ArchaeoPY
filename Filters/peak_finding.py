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

 
os.chdir('E:/CMD IP')

files = glob.glob('In' + '*' + '.png')

for fname in files:
    print fname
    im = Image.open(fname).convert('L')
    ary = np.array(im.getdata(), dtype=float).reshape(im.size[1], im.size[0])
    #ary = np.asarray(im.getdata())
    if '0.' in fname:
        ary = np.subtract(255, ary)
    ary = np.flipud(ary)
    #ary = np.abs(np.subtract(ary, 127.5))
    #ary = ansig(ary, 0.125, 0.125)
    imgplot = plt.imshow(ary, cmap = 'Greys', interpolation='none', aspect= 'equal', origin='upper')
    plt.show(block=True)
    plt.close()
    
    
    ##filtering parameters
    filter_size = [20,20]
    tharyhold = np.percentile(ary,80)
    
    cmap = cm.Greys
    cmap.set_bad('b',1.)  
    
    max_f = filters.maximum_filter(ary, size = filter_size)
    maxima = (ary == max_f)
    
    min_f = filters.minimum_filter(ary, size=filter_size)
    diff = ((max_f - min_f) > tharyhold)    
    maxima[diff == 0] = 0
    
    labeled, num_objects = ndimage.label(maxima)
    #, extent=[0.,y_int*ny,0.,x_int*nx], aspect= 'equal'
    imgplot = plt.imshow(ary, cmap = 'jet', interpolation='none')
    plt.savefig('GS.png', bbox_inches = 'tight')
    xy = np.array(ndimage.center_of_mass(ary, labeled, range(1, num_objects+1)))
    #World_addr =  os.path.splitext(fname)[0] + '.pgwx'
    World_addr = 'InPhase0.25m.png.cropped.pgwx'
    print World_addr
    cnt = (0,np.shape(ary)[1])
    xy_out = pixelToLatLon(World_addr,np.copy(xy),cnt)
    #xy_out = np.divide(xy, 10.64)
    #xy_out = Rotate2D(np.fliplr(xy_out), (0,0), np.deg2rad(32.0053832077))
    #xy_out = np.add(xy_out, (417944.79,443361.75))
    np.savetxt(fname + '.xy.csv', xy_out, delimiter=',', header='x,y', comments='')
    
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
    plt.savefig('aryult.png', bbox_inches = 'tight')
    plt.show(block=True)
    plt.close()