# -*- coding: utf-8 -*-
"""
Created on Thu Dec 11 01:00:29 2014

@author: FPopecarter
"""

import numpy as np
import glob, os

os.chdir('C:/data8')
#os.mkdir('temp')
files = glob.glob('HI' + '*' + '.Dat')

for fname in files:
    z = np.loadtxt(fname)
    
    a = np.arange(0,3200,1)
    b = np.repeat(np.arange(0,40,1), 80)[::-1]
    print b
    #print np.shape(a), np.shape(b), np.shape(z)
    
    ind = np.lexsort((a,b))
    print ind
    np.savetxt('temp/'+fname,z[ind])