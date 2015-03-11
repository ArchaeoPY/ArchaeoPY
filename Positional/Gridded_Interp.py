# -*- coding: utf-8 -*-
"""
Created on Wed Dec 10 16:44:27 2014

@author: FPopecarter
"""
import numpy as np
import matplotlib.pyplot as plt
HILO = 'LO' 
grid = '06'

fname = 'lister_vcp.csv'
array = np.genfromtxt(fname, dtype=float, delimiter=',', skiprows=1, filling_values=np.nan)

#Assume y is collumn 2
y = array[:,1]

#Assuming positions are 'non-interpolated'
#Finds lines where position is updated
changes = np.where(y[:-1] != y[1:])[0]
changes = np.concatenate(([0],changes))
#interpolates position between points
y_count = range(len(y))
new_y = np.interp(y_count,changes,y[changes+1])

#refills collumn 2 with updated y positions
array[:,1] = new_y

#np.savetxt(fname+'.csv', array, delimiter=',')

#duplicating windows into numpy array for no real reason...
x = array[:,0]
y = array[:,1]

#Traverses
#finds changes in 'x'
start = np.concatenate(([0],np.where(x[:-1] != x[1:])[0]+2))
stop = np.concatenate((np.where(x[:-1] != x[1:])[0],[-1]))
i=0

# 'output' data bounds
# Currently hardcoded
# need 'un' hardcoding
# first position, last position, number of readings

xstart = 0
xstop = 49
xreadings = 50

ystart = 0.125
ystop = 59.875
yreadings = 240

geoplotx = np.linspace(xstart,xstop,xreadings)
geoploty = np.linspace(ystart,ystop,yreadings)

array_size = np.empty([len(geoplotx), len(geoploty)])

print np.shape(array_size)

# prepopulates an empty numpy array to be filled with interpolated data
new_len = len(geoplotx)*len(geoploty)
out_array = np.empty((new_len,8))

print np.shape(out_array)

for start_x,stop_x in zip(start,stop):
    if i == xreadings:
        continue
    out_array[yreadings*i:yreadings*(i+1),0] = geoplotx[i]
    
    if i % 2 == 0:
        out_array[yreadings*i:yreadings*(i+1),1] = geoploty
    else:
        out_array[yreadings*i:yreadings*(i+1),1] = geoploty[::-1]
        
    j=2
    for collumn in out_array[:,2:].T:
        #print j
        if i % 2 == 0:
            #print j
            #print len(y[start_x:stop_x]), len(array[j,start_x:stop_x])
            collumn = np.interp(geoploty,y[start_x:stop_x],array[start_x:stop_x,j], right=np.nan, left=np.nan)
            #print geoploty
            #print y[start_x:stop_x]
            #print array[start_x:stop_x,j]
            #print collumn
        else:
            collumn = np.interp(geoploty,y[start_x:stop_x][::-1],array[start_x:stop_x,j][::-1], right=np.nan, left=np.nan)[::-1]
        out_array[yreadings*i:yreadings*(i+1),j] = collumn
        j+=1              
    i+=1
np.savetxt(fname+'rubberbanded.csv',out_array,delimiter=',')



fname_out = fname.split('.')[0]
for collumn, level in zip(out_array[:,2:].T,('c1','i1','c2','i2','c3','i3')):
    z = collumn
    for i in range(len(start)):
        if i % 2 != 0:
            z[yreadings*i:yreadings*(i+1)] = z[yreadings*i:yreadings*(i+1)][::-1]
    print HILO + level + '_' + str(grid) +'.DAT'
    np.savetxt(HILO + level + '_' + str(grid) +'.DAT',z)    
    #regrid = np.reshape(z, array_size)
    newz = z.reshape((len(geoplotx),len(geoploty)))
    np.savetxt('regridded'+HILO + level + '_' + str(grid) +'.txt',newz,delimiter='    ')
    neg_plt = np.median(z)-np.nanstd(z)
    print np.nanstd(z)
    print np.median(z)
    pos_plt = np.median(z)+np.nanstd(z)
    im = plt.imshow(newz, vmin=neg_plt, vmax=pos_plt, origin='upper', cmap=plt.cm.Greys,extent=(xstart,xstop,ystart,ystop))
    plt.colorbar()
     
    #plt.scatter(out_x,out_y)
    print 'image created'
    # print line
    plt.show(block=True)
    