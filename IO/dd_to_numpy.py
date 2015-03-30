from PIL import Image
import numpy as np

import matplotlib.pyplot as plt

#dd Image to Import
fname = 'DD20m-crop.PNG'

#Dimensions of Data in Readings
dimensions = (80,80)
#Threshold for converting grey to black/white (0-255)
bwthreshold = 100

#Opends Dot Density Image and converts to greyscale
dd_im = Image.open(fname, mode='r').convert('L')

#Converts PIL image object to numpy array
dd_array = np.array(dd_im, dtype=np.uint8)

#Makes copy of Dot Density Array
dd_bw_array = np.copy(dd_array)


dd_bw_array[dd_array>bwthreshold] = 0
dd_bw_array[dd_array<bwthreshold] = 1

#Creates empty output array
im_array = np.empty(dimensions, dtype = int)

in_shape = np.shape(dd_array)

#'bin' borders for converting pixels to values
xsa = np.round(np.linspace(0,in_shape[0], num =dimensions[0]+1))
ysa = np.round(np.linspace(0,in_shape[1], num =dimensions[1]+1))

#iterates through the empty output array
i=0
for xseg in xsa[0:dimensions[0]]:
    j=0
    for yseg in ysa[0:dimensions[1]]:
        #Calculates sum of segment bounded by 'bin' border
        im_array[i,j] = np.sum(dd_bw_array[xsa[i]:xsa[i+1],ysa[j]:ysa[j+1]])
        j+=1
    i+=1


vmin = np.percentile(im_array, 5)
vmax = np.percentile(im_array,95)

#uses matplotlib imshow to displayy data
plt.imshow(im_array,vmin = vmin, vmax = vmax, cmap = 'Greys', interpolation='kaiser')
plt.show()
        
