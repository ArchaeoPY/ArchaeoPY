# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 15:09:47 2015

@author: Hannah
"""

from PIL import Image
import numpy as np
import pylab
import os

from ArchaeoPY.IO.image import lum2png

def pca(X):
  # Principal Component Analysis
  # input: X, matrix with training data as flattened arrays in rows
  # return: projection matrix (with important dimensions first),
  # variance and mean

  #get dimensions
  num_data,dim = X.shape

  #center data
  mean_X = X.mean(axis=0)
  for i in range(num_data):
      X[i] -= mean_X

  if dim>100:
      print 'PCA - compact trick used'
      M = np.dot(X,X.T) #covariance matrix
      e,EV = np.linalg.eigh(M) #eigenvalues and eigenvectors
      tmp = np.dot(X.T,EV).T #this is the compact trick
      V = tmp[::-1] #reverse since last eigenvectors are the ones we want
      S = np.sqrt(e)[::-1] #reverse since eigenvalues are in increasing order
  else:
      print 'PCA - SVD used'
      U,S,V = np.linalg.svd(X)
      V = V[:num_data] #only makes sense to return the first num_data

  #return the projection matrix, the variance and the mean
  return V,S,mean_X

#List of Images to combine (must be 'same' tile)  
imlist = ('lidar_01_01.png', 'lidar2_01_01.png')
#changes directory to 'Data' directory
os.chdir('../../Data')

#opens image to get image size
im = np.array(Image.open(imlist[0]))
#open one image to get the size
m,n = im.shape[0:2] #get the size of the images

#makes a copy of original image touse as mask later
#255 appears to be 'nodata'
mask = np.copy(im)

imnbr = len(imlist) #get the number of images

#create matrix to store all flattened images
immatrix = np.array([np.array(Image.open(imlist[i]),dtype=float).flatten() for i in range(imnbr)],'f')

#perform PCA
V,S,immean = pca(immatrix)
print np.shape(V)
print S

#mean image and first mode of variation
immean = immean.reshape(m,n)
mode = V[0].reshape(m,n)

#masks PDA'd data using mask from earlier
mode[mask==255]=np.nan

#show the images
pylab.figure()
pylab.gray()
pylab.imshow(immean)

pylab.figure()
pylab.gray()
pylab.imshow(V[1].reshape(m,n))

pylab.figure()
pylab.gray()
pylab.imshow(mode)

pylab.show()

#saves data using archaeopy lum2png
fname = 'mode'+imlist[0]
lum2png(mode,fname)


