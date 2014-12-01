from skimage import exposure, filter, feature
from skimage.color import rgb2gray

'''Information and functions taken from scikit-image. Please consult 
scikit-image.org/docs for further information.'''

'''Contrast Limited Adaptive Histogram Equalization
(input array, clip limit = between 0 and 1--higher values gives more contrast)
Returns equalized image as ndarray'''
def adapteq(array):
    return exposure.equalize_adapthist(array, clip_limit=0.03)

'''Applies a local or dynamic threshold to an array.
The threshold value is the weighted mean for the local neighborhood of a pixel 
subtracted by a constant'''  
def adaptthreshold(array):
    return filter.threshold_adaptive(array, 40, 'gaussian')

'''Edge filter using the Canny algorithm
(input array, sigma = SD of gaussian filter)'''
def cannyfilter(array):
    grayarray = rgb2gray(array)
    return feature.canny(grayarray, sigma=1)