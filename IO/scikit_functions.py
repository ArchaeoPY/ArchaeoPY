from skimage import exposure, filter
import numpy as np
from skimage import img_as_float, io
import matplotlib.pyplot as plt

def adapteq(array):
    return exposure.equalize_adapthist(array, clip_limit=0.03)
   
def adaptthreshold(array):
    return filter.threshold_adaptive(array, 40, 'gaussian')

