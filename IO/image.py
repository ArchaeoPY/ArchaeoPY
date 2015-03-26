# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 16:15:46 2015

@author: FPopecarter
"""
from PIL import Image
import numpy as np
def lum2png(comp,filename):
    L = 255
    A = np.zeros(np.shape(comp))
    A.fill(255)

    masked = np.ma.masked_array(comp,np.isnan(comp))
    masked2 = np.ma.masked_array(A, mask=np.isnan(comp), fill_value=0)
    masked2 = masked2.filled(0)
    #masked2 = np.flipud(masked2)

    np.array(masked)
    #comp = np.flipud(comp)
    Min = np.nanmin(comp)
    Max = np.nanmax(comp)
    print Min, Max
    Range = float(Max - Min)
    scale = 255.0/Range
    comp = comp - Min
    comp = comp*scale
    comp = comp + (255 - 2*comp)

    l  = comp

    new_comp = np.array([l,masked2])
    new_comp = np.rollaxis(new_comp,-1)
    new_comp = np.rollaxis(new_comp,-1)

    #print new_comp.shape
    im = Image.fromarray(np.uint8(new_comp), "LA" )
    
    png_info = im.info

    im.save(filename, quality=100, **png_info)
