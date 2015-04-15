# -*- coding: utf-8 -*-
"""
Created on Wed Dec 10 16:44:27 2014

Regridding CMD (xyz) Data

@author: FPopecarter and CHarris

Written for regridding CMD Mini Explorer (traversessamplesz) data. As written, accept data traverses, samples, z data in 
comma separated columns where the samples values are not interpolated down the line.
For reference, see "example file" in ArchaeoPY - Data folder. Rubber bands the 
data points along the line, then applies a linear interpolation--from the 
"traverses_start, traverses_stop, traverses_readings" and "samples_start, samples_stop, samples_readings" variables. 

Finally, exports the data in two formats:
1) z data with .dat extension
2) regridded tab separated spreadsheet data 

Both of these formats can be imported into Geoplot, with the dummy values set to 
2047.5 
"""

import numpy as np
import matplotlib.pyplot as plt
#np.set_printoptions(threshold=np.nan)

'''File Properties'''
HILO = 'LO' #Coil Orientation
grid = 'All' #Grid Number

fname = 'linton vcp 2 fixed.csv'
f = open(fname, 'r')
#no_cols = len(f.readline().split(','))
array = np.genfromtxt(f, dtype=float, delimiter=',', skiprows=1, filling_values=np.nan)
print np.shape(array)
#duplicating windows into numpy array for clarity stake.
traverses = array[:,0]
samples = array[:,1]
num_cols = 8

'''Survey Properties'''
# Currentlsamples hardcoded
# need 'un' hardcoding
# first position, last position, number of readings
samples_start = 0.125
samples_stop = 59.875
no_samples = 240

traverses_start = 20.5
traverses_stop = 39.5
no_traverses = 20


'''Fixing the blank row at the end of a line:'''
#Identify line changes
traverse_changes = np.where(traverses[:-1] != traverses[1:])[0]
stop = traverse_changes #End of Line
#last_row = len(samples)
#stop = np.append(stop, last_row)
start = np.concatenate(([0],np.add(stop,1))) #Beginning of Line

#shifts 'end' sample back one place
samples[stop-1] = samples[stop]
samples[stop] = np.nan
last_row = len(samples)-1
samples[last_row-1] = 0
samples[last_row] = np.nan
array[:,1] = samples

#creates new array without 'blank' rows (at the end of lines)
array = np.copy(array[np.isfinite(samples),:])
#np.savettraversest(fname+'out.csv', arrasamples, delimiter=',')


''' Rubberbanding readings down the line:'''
#duplicating windows into numpy arrays for clarity
traverses = array[:,0]
samples = array[:,1]

#Assuming positions are 'non-interpolated'
#Finds lines where position is updated
changes = np.add(np.where(samples[:-1] != samples[1:])[0],1)
changes = np.concatenate(([0],changes))

#interpolates position between points
samples_count = range(len(samples))
samples_count = np.array(samples_count)
#np.savetxt('samples_count.csv', samples_count, delimiter=',')
samples = np.interp(samples_count,changes,samples[changes])
#np.savetxt('samples.csv', samples, delimiter = ',')
array[:,1] = samples #Updates y-positions to inteprolated points
np.savetxt(fname+'_rubberbanded.csv', array, delimiter=',')


'''Regridding'''
#Traverses
#finds changes in 'traverses' with the new updated dataset, for regridding
start = np.concatenate(([0],np.where(traverses[:-1] != traverses[1:])[0]))+1
stop = np.concatenate((np.where(traverses[:-1] != traverses[1:])[0],[-1]))
#last_reading = len(samples)-1
#last_stop = len(stop)-1
#stop[last_stop] = last_reading
#print start
i=0

#Creating a grid of positions
geoplot_traverses = np.linspace(traverses_start,traverses_stop,no_traverses)

geoplot_samples = np.linspace(samples_start,samples_stop,no_samples)


# prepopulates an empty numpy array to be filled with interpolated data
new_len = len(geoplot_samples)*len(geoplot_traverses)
out_array = np.empty((new_len,num_cols))

'''Resamples data onto 'new' grid
First reading of the file is dropped---needs fixing'''
#Iterates through the datasets
for start_traverses,stop_traverses in zip(start,stop):
    if i == no_traverses:
        continue
    out_array[no_samples*i:no_samples*(i+1),0] = geoplot_traverses[i]
    print out_array[no_samples*i:no_samples*(i+1),0]
    
    if i % 2 == 0:
        out_array[no_samples*i:no_samples*(i+1),1] = geoplot_samples
    else:
        out_array[no_samples*i:no_samples*(i+1),1] = geoplot_samples[::-1]
        
    j=2
    for column in out_array[:,2:].T:
        if i % 2 == 0:
            column = np.interp(geoplot_samples,samples[start_traverses:stop_traverses],
                               array[start_traverses:stop_traverses,j])

        else:
            column = np.interp(geoplot_samples,samples[start_traverses:stop_traverses][::-1], 
                               array[start_traverses:stop_traverses,j][::-1])[::-1]
        out_array[no_samples*i:no_samples*(i+1),j] = column
        j+=1  
        #print start_traverses            
    i+=1
np.savetxt(fname+'_resampled.csv',out_array,delimiter=',')


'''Saves Data Out'''
fname_out = fname.split('.')[0]
for column, level in zip(out_array[:,2:].T,('C1','I1','C2','I2','C3','I3')):    
    z = column
    #print column
    for i in range(len(start)):
        if i % 2 != 0:
            #print no_samples*i,no_samples*(i+1)
            #print np.shape(z)
            z[no_samples*i:no_samples*(i+1)] = z[no_samples*i:no_samples*(i+1)][::-1]
    #print HILO + level + '_' + str(grid) +'.DAT'
    np.savetxt(HILO + level + '_' + str(grid) +'.DAT',z)  
    #print z
    #print len(z)
    #regrid = np.reshape(z, arrasamples_size)
    newz = z.reshape((len(geoplot_traverses),len(geoplot_samples)))
    #print np.shape(newz)    
    np.savetxt('regridded'+HILO + level + '_' + str(grid) +'.csv',newz,delimiter=',')
    neg_plt = np.nanmedian(z)-np.nanstd(z)
    #print np.nanstd(z)
    #print np.nanmedian(z)
    fig = plt.figure()
    #atraverses = fig.add_atraverseses([0.05,0.05,0.9,0.9])
    pos_plt = np.nanmedian(z)+np.nanstd(z)
    #atraverses.atraversesis('equal')
    im = plt.imshow(newz, vmin=neg_plt, vmax=pos_plt, interpolation='nearest',
                    origin="upper", cmap=plt.cm.Greys, extent=(samples_start,samples_stop,traverses_start,traverses_stop))
    plt.colorbar()
     
    #plt.scatter(out_traverses,out_samples)
    print 'image created'
    # print line
    plt.show(block=True)
    