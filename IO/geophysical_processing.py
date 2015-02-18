import numpy as np
import numpy.ma as ma
import scipy
import scipy.ndimage as im

def interpolate_nn(coordinates, array):
    return scipy.interpolate.NearestNDInterpolator(coordinates, array)

def crop(array):
    ma.masked_equal(array, 2047.5)

def median_filter(array):
    return im.median_filter(array, size=(2, 2))         