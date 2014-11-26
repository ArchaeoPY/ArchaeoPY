from skimage import exposure
import numpy as np

def adaptive_equalisation (fname, bins=256):
    p2, p98 = np.percentile(fname,(2,98) )
    img = exposure.rescale_intensity(fname, in_range=(p2, p98))
    return img


    