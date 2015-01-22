# -*- coding: utf-8 -*-
"""
Created on Wed Dec 10 16:44:27 2014

@author: FPopecarter
"""
import numpy as np
HILO = 'LO' 
grid = '06'

fname = 'E:/MENSTON/MenLo6.csv'
array = np.genfromtxt(fname, dtype=float, delimiter=',', skiprows=1, filling_values=np.nan)

print array
y = array[:,1]
changes = np.where(y[:-1] != y[1:])[0]
changes = np.concatenate(([0],changes))

y_count = range(len(y))
new_y = np.interp(y_count,changes,y[changes+1])

array[:,1] = new_y

#np.savetxt(fname+'.csv', array, delimiter=',')
x = array[:,0]
y = array[:,1]

#Traverses
start = np.concatenate(([0],np.where(x[:-1] != x[1:])[0]+2))
stop = np.concatenate((np.where(x[:-1] != x[1:])[0],[-1]))
i=0

geoplotx = np.linspace(0.25,19.75,40)
geoploty = np.linspace(0.125,19.875,80)
#print start
#print stop
new_len = len(geoplotx)*len(geoploty)

out_array = np.empty((new_len,8))

for start_x,stop_x in zip(start,stop):
    if i == 40:
        continue
    out_array[80*i:80*(i+1),0] = geoplotx[i]
    
    if i % 2 == 0:
        out_array[80*i:80*(i+1),1] = geoploty
    else:
        out_array[80*i:80*(i+1),1] = geoploty[::-1]
        
    j=2
    for collumn in out_array[:,2:].T:
        #print j
        if i % 2 == 0:
            print j
            #print len(y[start_x:stop_x]), len(array[j,start_x:stop_x])
            collumn = np.interp(geoploty,y[start_x:stop_x],array[start_x:stop_x,j])
            #print geoploty
            #print y[start_x:stop_x]
            #print array[start_x:stop_x,j]
            #print collumn
        else:
            collumn = np.interp(geoploty,y[start_x:stop_x][::-1],array[start_x:stop_x,j][::-1])[::-1]
        out_array[80*i:80*(i+1),j] = collumn
        j+=1              
    i+=1
np.savetxt(fname+'gridded.csv',out_array,delimiter=',')

fname_out = fname.split('.')[0]
for collumn, level in zip(out_array[:,2:].T,('c1','i1','c2','i2','c3','i3')):
    z = collumn
    for i in range(len(start)):
        if i % 2 != 0:
            z[80*i:80*(i+1)] = z[80*i:80*(i+1)][::-1]
    print HILO + level + '_' + str(grid) +'.DAT'
    np.savetxt(HILO + level + '_' + str(grid) +'.DAT',z)    
    
    