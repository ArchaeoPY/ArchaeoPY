from skimage import exposure
import numpy as np
from skimage import img_as_float, io
import matplotlib.pyplot as plt

def intensity_rescale(array):
    p2, p98 = np.percentile(array,(2,98))
    img = exposure.rescale_intensity(array, in_range=(p2, p98))
    return img


