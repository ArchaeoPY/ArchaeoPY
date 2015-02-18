# -*- coding: utf-8 -*-
"""
Created on Fri Jan 23 09:20:45 2015

@author: FPopecarter
"""

from PIL import Image
import numpy as np


def array2image(comp,Max,Min,out_filename, x_space, y_space, interp=Image.BICUBIC):
    R = 255
    G = 255
    B = 255
    A = np.zeros(np.shape(comp))
    A.fill(255)
    print np.shape(comp)
    
    #Make dummy Values Nan
    comp[comp==2047.5] = np.nan
    masked = np.ma.masked_array(comp,np.isnan(comp))
    masked2 = np.ma.masked_array(A, mask=np.isnan(comp), fill_value=0)
    masked2 = masked2.filled(0)
#    masked2 = np.flipud(masked2)
    
    
    #Clip data to positive / negative plotting thresholds
    #Not sure why out is masked, possibly memory?
    comp =  np.clip(masked, float(Min), float(Max), out=masked)
#    comp = np.flipud(comp)
    Min = comp.min()
    Max = comp.max()
    
    #Scale data to fill positive / negative thresholds
    Range = float(Max - Min)
    scale = 255.0/Range
    comp = comp - Min
    comp = comp*scale
    comp = comp + (255 - 2*comp)

    #Fill RGB arrays
    r  = comp.filled(R)
    g  = comp.filled(G)
    b  = comp.filled(B)

    #masked2 is alpha channel
    new_comp = np.array([r,g,b,masked2])
    new_comp = np.rollaxis(new_comp,-1)
    new_comp = np.rollaxis(new_comp,-1)

    #Create Image from RGBA Array
    im = Image.fromarray(np.uint8(new_comp), "RGBA" )
    
    #calculates size required for square pixels
    width, height = im.size
    height = (y_space/x_space)*height
    height = int(height)
    
    #resizes image using required interpolation method
    im = im.resize((width, height), interp)
    
    #Saves image out as PNG
    png_info = im.info
    im.save(str(out_filename), format ='PNG', quality=100)
    
    return