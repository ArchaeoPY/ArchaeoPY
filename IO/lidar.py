import numpy as np
from skimage import img_as_float, io
from PIL import Image
import os
import image_slicer

os.chdir('../../Data')

image_slicer.slice('lidar2.png', 100)
image_slicer

stop

im = Image.open('lidar.png').convert("L")
array1 = np.ma.array(im)
array1[array1==255]=np.ma.masked
print array1.shape
print array1
#np.save('array1',array1)

im2 = Image.open('lidar2.png').convert("L")
array2 = np.ma.array(im2)
array2[array2==255]=np.ma.masked
print array2.shape
print array2
#np.save('array1',array1)

array3 = np.add(array1, array2)
print 'add'
array3 = np.divide(array3, 2)
print'divide'

img3 = Image.fromarray(array3)
print 'made image'

img3.save('lidar3.png')

'''
f = open('lidar.png', 'rb')
image1 = io.imread(f)
array1 = img_as_float(image1)
np.save('array1', array1)


f = open('lidar2.png', 'rb')
image2 = io.imread(f)
array2 = img_as_float(image2)
np.save('array2', array2)
print "Done! :)"

'''