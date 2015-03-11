import numpy as np
from skimage import img_as_float, io
from PIL import Image

im = Image.open('lidar.png').convert("L")
array1 = np.array(im)
print array1.shape
print array1
#np.save('array1',array1)

im2 = Image.open('lidar2.png').convert("L")
array2 = np.array(im2)
print array2.shape
print array2
#np.save('array1',array1)

array3 = np.add(array1, array2)
array3 = np.divide(array3, 2)

img3 = Image.fromarray(array3)

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