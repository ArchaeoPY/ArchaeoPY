# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 15:09:47 2015

@author: Hannah
"""

from PIL import Image
import numpy as np
import pylab
import os

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
  
imlist = ('lidar_01_01.png', 'lidar2_01_01.png')
os.chdir('../../Data')

im = np.array(Image.open(imlist[0])) #open one image to get the size
m,n = im.shape[0:2] #get the size of the images
imnbr = len(imlist) #get the number of images

#create matrix to store all flattened images
immatrix = np.array([np.array(Image.open(imlist[i])).flatten() for i in range(imnbr)],'f')

#perform PCA
V,S,immean = pca(immatrix)

#mean image and first mode of variation
immean = immean.reshape(m,n)
mode = V[0].reshape(m,n)

#show the images
pylab.figure()
pylab.gray()
pylab.imshow(immean)

pylab.figure()
pylab.gray()
pylab.imshow(mode)

pylab.show()
print mode
immode = Image.fromarray(mode)
fname = 'mode'+imlist[0]
immode.save(fname)

