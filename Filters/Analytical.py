# -*- coding: utf-8 -*-
"""
Created on Mon Dec 08 15:10:46 2014

@author: FPopecarter
"""
from shapely.geometry import mapping, Point
import fiona

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import scipy.ndimage as ndimage
import scipy.ndimage.filters as filters

from ArchaeoPY.Positional.points import Rotate2D

from PIL import Image

def ansig(data, x_int, y_int):

    dx, dy, dz = derivxyz(data, x_int, y_int)

    res = np.sqrt(dx**2 + dy**2 + dz**2)
    return res
    
def derivxyz(data, x_int, y_int, order=1):
    Fx, Fy = wv_numbers(data, x_int, y_int)
    Fz = np.sqrt(np.square(Fx)+np.square(Fy))
    
    Fx, Fy = wv_numbers(data, x_int, y_int)
    Fx, Fy = Fx * 1j, Fy * 1j
    
    Dx = fft_derivative(Fx, data, order)
    Dy = fft_derivative(Fy, data, order)
    Dz = fft_derivative(Fz, data, order)
    
    return Dx, Dy, Dz
    
    
def wv_numbers(array, x_space, y_space):
    """
    Get two 2D-arrays with the wave numbers in the x and y directions.
    """
    ny, nx = np.shape(array)
    dx = float(x_space*nx)/float(nx - 1)
    fx = np.fft.fftfreq(nx, dx)
    dy = float(y_space*ny)/float(ny - 1)
    fy = np.fft.fftfreq(ny, dy)
    return np.meshgrid(fx, fy)
    
def fft_derivative(freqs, data, order):
    """
    Calculate a generic derivative using the FFT.
    """
    mean = np.round(np.nanmean(data), 2)
    nan_filler = float(str(mean)+'2047')
    print nan_filler
    data[np.isnan(data)]=nan_filler
    fgrid = (2.*np.pi)*np.fft.fft2(data)
    deriv = np.real(np.fft.ifft2((freqs**order)*fgrid))
    deriv[data==nan_filler]=np.nan
    return deriv
    
if __name__ == '__main__':
    fname =  'C:/Users/fpopecarter.GSBPROSPECTION/GSB Google Drive/Cart Data/Bradford/Menston/Menston_1_/z.txt'
    array = np.genfromtxt(fname, dtype=float)
    #array = np.flipud(array)
    y_int = 0.125
    x_int = 0.75
    nx, ny = np.shape(array)
    print nx, ny
    res = ansig(array, y_int, x_int)
    np.savetxt('temp.txt', res)    
    
    vmin = np.percentile(res[np.isfinite(res)], 10)
    vmax = np.percentile(res[np.isfinite(res)], 90)
    
    print x_int*nx
    print y_int*ny
    
    cmap = cm.jet
    cmap.set_bad('w',1.)    
    
    imgplot = plt.imshow(res, cmap = cmap, vmin=vmin, vmax = vmax, interpolation='none', extent=[0.,y_int*ny,0.,x_int*nx], aspect= 'equal', origin='lower')
    plt.savefig('Analtyical.png', bbox_inches = 'tight')    
    plt.show(block=True)
    plt.close()
    
    print np.shape(res)    
    
    #rescale data
    mask = np.ones(np.shape(res), dtype=int)
    nan_filler = float(str(np.nanmean(res))+'2047')
    mask[np.isnan(res)] = 0
    res[np.isnan(res)]=nan_filler
    array[np.isnan(res)]=nan_filler
    res = ndimage.zoom(res, (6,1.0))
    mask = ndimage.zoom(mask, (6,1.0))
    array = ndimage.zoom(array, (6,1.0))
    res[mask==0] = np.nan
    array[mask==0] = np.nan
    
    print np.shape(res)
    
    out = np.subtract(np.copy(res), np.percentile(np.isfinite(res),10))
    out = np.divide(out,np.percentile(res[np.isfinite(res)], 90))
    out = np.flipud(out)
    im = Image.fromarray(np.uint8(cmap(out)*255))
    im.save('Analytical.png')
    
    imgplot = plt.imshow(res, cmap = cmap, vmin=vmin, vmax = vmax, interpolation='none', extent=[0.,y_int*ny,0.,x_int*nx], aspect= 'equal', origin='lower')
    #plt.savefig('Analtyical.png', bbox_inches = 'tight')    
    plt.show(block=True)
    plt.close()
    
    ##filtering parameters
    filter_size = [15,15]
    threshold = np.percentile(res,80)
    
    cmap = cm.Greys
    cmap.set_bad('b',1.)  
    
    max_f = filters.maximum_filter(res, size = filter_size)
    maxima = (res == max_f)
    
    min_f = filters.minimum_filter(res, size=filter_size)
    diff = ((max_f - min_f) > threshold)    
    maxima[diff == 0] = 0
    
    labeled, num_objects = ndimage.label(maxima)
    #, extent=[0.,y_int*ny,0.,x_int*nx], aspect= 'equal'
    imgplot = plt.imshow(array, cmap = cmap, vmin=-10, vmax = 10, interpolation='none')
    plt.savefig('GS.png', bbox_inches = 'tight')
    xy = np.array(ndimage.center_of_mass(res, labeled, range(1, num_objects+1)))
    
    xy_out = np.divide(xy, 10.64)
    xy_out = Rotate2D(np.fliplr(xy_out), (0,0), np.deg2rad(32.0053832077))
    xy_out = np.add(xy_out, (417944.79,443361.75))
    np.savetxt('xy.csv', xy_out, delimiter=',', header='x,y', comments='')
    
    schema = {
        'geometry': 'Point',
        'properties': {'id':'int'},
    }
    i = 0
    with fiona.open('xy.shp', 'w', 'ESRI Shapefile', schema) as c:
        for row in xy_out:
            point = Point(row)
            c.write({
            'geometry':mapping(point),
            'properties': {'id':i},
            })
            i += 1
    
    plt.savefig('Points.png', bbox_inches = 'tight')
    plt.autoscale(False)
    plt.plot(xy[:, 1], xy[:, 0], 'bo')
    plt.savefig('result.png', bbox_inches = 'tight')
    plt.show(block=True)
    plt.close()
    
    #vmin = np.percentile(max_f[np.isfinite(res)], 5)
    #vmax = np.percentile(max_f[np.isfinite(res)], 95)
    #imgplot = plt.imshow(max_f, cmap = cmap, vmin=vmin, vmax = vmax, interpolation='none', extent=[0.,y_int*ny,0.,x_int*nx], aspect= 'equal', origin='lower')
    #plt.show(block=True)
    