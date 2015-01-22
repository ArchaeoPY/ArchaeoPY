# -*- coding: utf-8 -*-
"""
Created on Thu Dec 11 14:21:26 2014

@author: FPopecarter
"""

import numpy as np
import glob, os
from PIL import Image

os.chdir('C:/GeoSuB/Outputs/Menston Images/Twin Probe')
#os.mkdir('temp')

directory = 'Twin Probe'
html = open('html.txt', 'w')
layers = open('layers.txt','w')
         
types = ('*.png', '*.bmp', '*.jpg') # the tuple of file types
files = []
for ext in types:
    files.extend(glob.glob(ext))

for fname in files:
    print fname
    #img = Image.open(fname).convert('LA')
    #img.save(fname)
    #w_fname = fname + 'w'
    gtif_n = os.path.splitext(fname)[0] + '.tif'
    '''
    D = 0.2106859598939696
    B = 0.2106859598939696
    
    C = 417964.42549261334
    F = 443383.78862476966
    
    A = -0.13457869929445174
    E = 0.13457869929445174
    
    w_obj = open(w_fname, 'w+')
    print>>w_obj,A
    print>>w_obj,D
    print>>w_obj,B
    print>>w_obj,E
    print>>w_obj,C
    print>>w_obj,F
    
    w_obj.close()
    '''
    layer = os.path.splitext(fname)[0]
    layer = layer.translate(None, '-.')
    
    string = 'gdal_translate %s %s'%(fname,gtif_n)
    os.system(string)
    
    path = directory + '/' + os.path.splitext(fname)[0]

    if layer[3] == 'H':
        c_type = 'Horiz '
    else:
        c_type = 'Vert '
        
        
    layer_text = 'CMD ' + c_type + layer[4] + ' ' + layer[5]

    print>>html, '                  // create TMS Overlay layer'
    print>>html, '                   var %s = new OpenLayers.Layer.TMS("%s", "",' %(layer, layer_text)
    print>>html, '                  {'
    print>>html, "                      serviceVersion: '.',"
    print>>html, "                      layername: '%s'," %path
    print>>html, "                      alpha: true,"
    print>>html, "                      type: 'png',"
    print>>html, "                      isBaseLayer: false,"
    print>>html, "                      getURL: getURL"
    print>>html, '                  });'
    print>>html, '                  if (OpenLayers.Util.alphaHack() == false) {'
    print>>html, '                      %s.setOpacity(1.0);' %layer
    print>>html, '                  }'


    print>>layers, '%s,' %layer

    string ="C:/OSGeo4W64/bin/gdal2tiles.py -e -r antialias -z 16-22 -s EPSG:27700  %s"%(gtif_n)
    os.system(string)
html.close()