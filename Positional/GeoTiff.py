# -*- coding: utf-8 -*-
"""
Created on Fri Jun 20 09:48:48 2014

@author: FPopecarter
"""

import simplekml
import scipy
import numpy as np
import pyproj
import boto
import uuid
import random, string
import os
import time
import hashlib
import glob
from osgeo import osr,gdal
import gdal_merge
import shutil

from StringIO import StringIO
from boto.s3.connection import S3Connection


from PIL import Image

from math import *

def numTiles(z):
  return(pow(2,z))

def sec(x):
  return(1/cos(x))

def latlon2relativeXY(lat,lon):
  x = (lon + 180) / 360
  y = (1 - log(tan(radians(lat)) + sec(radians(lat))) / pi) / 2
  return(x,y)

def latlon2xy(lat,lon,z):
  n = numTiles(z)
  x,y = latlon2relativeXY(lat,lon)
  return(n*x, n*y)
  
def tileXY(lat, lon, z):
  x,y = latlon2xy(lat,lon,z)
  return(int(x),int(y))

def xy2latlon(x,y,z):
  n = numTiles(z)
  relY = y / n
  lat = mercatorToLat(pi * (1 - 2 * relY))
  lon = -180.0 + 360.0 * x / n
  return(lat,lon)
  
def latEdges(y,z):
  n = numTiles(z)
  unit = 1 / n
  relY1 = y * unit
  relY2 = relY1 + unit
  lat1 = mercatorToLat(pi * (1 - 2 * relY1))
  lat2 = mercatorToLat(pi * (1 - 2 * relY2))
  return(lat1,lat2)

def lonEdges(x,z):
  n = numTiles(z)
  unit = 360 / n
  lon1 = -180 + x * unit
  lon2 = lon1 + unit
  return(lon1,lon2)
  
def tileEdges(x,y,z):
  lat1,lat2 = latEdges(y,z)
  lon1,lon2 = lonEdges(x,z)
  return((lat2, lon1, lat1, lon2)) # S,W,N,E

def mercatorToLat(mercatorY):
  return(degrees(atan(sinh(mercatorY))))

def tileSizePixels():
  return(256)

def tileLayerExt(layer):
  if(layer in ('oam')):
    return('jpg')
  return('png')
  
  
def slippy_bbox(bbox,zbox,image_object):
    '''
    Bounding box of image in latitude, longtiude
    as tuple (SW, SE, NE, NW)
    
    Bounding Z levels as slippy zooms
    '''
    min_x = min((bbox[0][1],bbox[1][1],bbox[2][1].bbox[3][1]))
    max_x = max((bbox[0][1],bbox[1][1],bbox[2][1].bbox[3][1]))
    
    min_y = min((bbox[0][0],bbox[1][0],bbox[2][0].bbox[3][0]))
    min_y = max((bbox[0][0],bbox[1][0],bbox[2][0].bbox[3][0]))
    
    im_length, im_height = image_object.size
    length = max_x - min_x
    #calculates the slippy xy bounds for lowest zoom level
    ll_x, ll_y = latlon2xy(min_x,min_y,zbox[-1])
    ur_x, ur_y = latlon2xy(max_x,max_y,zbox[-1])
    
    new_pixel_length = ((ur_x-ll_x)*256,(ur_y-ll_y)*256)
    new_bbox = (tileEdges(ll_x,ll_y,zbox[-1]),tileEdges(ur_x,ur_y,zbox[-1]))
    new_length = new_bbox[1][0] - new_bbox[0][0]

    scale = new_length / new_pixel_length
    
    size = im_length * scale, im_height * scale
    image_object.thumbnail(size, Image.ANTIALIAS)
    

def md5_from_filename(fileName, block_size=2**14):
    md5 = hashlib.md5()
    f = open(fileName)
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)
    f.close()
    return md5.hexdigest()
    
    
def XY_To_LL(x, y):
    wgs84=pyproj.Proj("+init=EPSG:4326")
    osgb36=pyproj.Proj("+init=EPSG:27700")

    lon,lat = pyproj.transform(osgb36,wgs84, x,y)
    
    return lon,lat

def Rotate2D(pts,cnt,ang=scipy.pi/4):
    '''pts = {} Rotates points(nx2) about center cnt(2) by angle ang(1) in radian'''
    pi     = scipy.pi
    dot    = scipy.dot
    sin    = scipy.sin
    cos    = scipy.cos
    ar     = scipy.array
    rand   = scipy.rand
    arange = scipy.arange
    return dot(pts-cnt,ar([[cos(ang),sin(ang)],[-sin(ang),cos(ang)]]))+cnt

#Initiates two kml's, one low res for mobile
kml = simplekml.Kml()
m_kml = simplekml.Kml()

#Creates a new folder and prevents the user from looking inside
#used to prevent the logo being disabled
folder = kml.newfolder(name='CartEasyN')
m_folder = m_kml.newfolder(name='CartEasyN')

#Hides folders from prying eyes..
folder.liststyle.listitemtype = "checkHideChildren"
m_folder.liststyle.listitemtype = "checkHideChildren"


#####*************************************###########
#Company Name
# GSB/ Stratascan

company = 'Bradford'
#KML Job name
job = 'Menston'

pos_plot = 10
neg_plot = -10

#####*************************************###########
Directory = "Cart Data/" + str(company) + "/" + str(job)
os.chdir(Directory)

location_str = '*location+'+'*'+'.txt'
projects = glob.glob('*'+job+'*')

filenames = []
locations = []
layers = []

for line in projects:
    print line
    line=str(line)
    #file_temp = line + "/" + line + "-2_to_3.png"
    file_temp = line + "/" + line + str(neg_plot)+"_to_"+ str(pos_plot) + ".png"
    if os.path.isfile(file_temp):
        location_temp = line + "/location_" + line + ".txt"
        if os.path.isfile(location_temp):
            filenames.append(file_temp)
            locations.append(location_temp)
            layers.append(line)
            print file_temp
            print location_temp
            print file_temp
    
#sets up a few variables required later
bb_x = np.empty(0, dtype=float)
bb_y = np.empty(0, dtype=float)

#Add Logo as screenoverlay
logo_url = 'https://s3.amazonaws.com/kml-test.carteasyn.com/logo/carteasyn-gsb.png'
screen = folder.newscreenoverlay(name='ScreenOverlay')
m_screen = m_folder.newscreenoverlay(name='ScreenOverlay')
screen.icon.href = logo_url
m_screen.icon.href = logo_url

#sets location, overlayxy is position on image, screenxy corresponding screen position
screen.overlayxy = simplekml.OverlayXY(x=0.5,y=0,xunits=simplekml.Units.fraction,
                                       yunits=simplekml.Units.fraction)
screen.screenxy = simplekml.ScreenXY(x=0.91,y=0.12,xunits=simplekml.Units.fraction,
                                     yunits=simplekml.Units.fraction)
                                     
m_screen.overlayxy = simplekml.OverlayXY(x=0.5,y=0,xunits=simplekml.Units.fraction,
                                       yunits=simplekml.Units.fraction)
m_screen.screenxy = simplekml.ScreenXY(x=0.91,y=0.12,xunits=simplekml.Units.fraction,
                                     yunits=simplekml.Units.fraction)
#Image size & units
screen.size.x = 180
screen.size.y = 120
screen.size.xunits = simplekml.Units.pixel
screen.size.yunits = simplekml.Units.pixel

m_screen.size.x = 180
m_screen.size.y = 120
m_screen.size.xunits = simplekml.Units.pixel
m_screen.size.yunits = simplekml.Units.pixel

#Connects to Amazon 3 user credentials
conn = S3Connection('AKIAIJ5XGETIQYT2KSCA', 'P6K/mqXzE/y09zbCQoj06BQJ3rUPQpKPauoclyMX')

GDal_merge_string = ''

#iterates through fields & layers
for filename, location, layer in zip(filenames,locations, layers):
    time.sleep(1)
    #filename = "C:/Users/fpopecarter.GSBPROSPECTION/GSB Google Drive/Cart Data/Ashton/Ashton_9_/Ashton_9_-1_to_2.png"
    #location = 'C:/Users/fpopecarter.GSBPROSPECTION/GSB Google Drive/Cart Data/Ashton/Ashton_9_/location_Ashton_9_.txt'
    
    image_obj = Image.open(filename, mode='r')
    x_pix, y_pix = image_obj.size
    #image_obj.close()
    
    mobile_img = image_obj.resize((x_pix/2, y_pix/2), Image.ANTIALIAS)
    m_filename = filename.split('.')[0]+'mobile.png'
    print m_filename
    mobile_img.save(m_filename)
    #print x_pix, y_pix
    
    location_obj = open(location, 'r')
    
    x_min = float(location_obj.readline().split(' ')[1])
    y_min = float(location_obj.readline().split(' ')[1])
    
    x_length = float(location_obj.readline().split(' ')[1])
    rotation = float(location_obj.readline().split(' ')[1])
    
    #Defines Bounding Box corners
    pix_length = x_length / x_pix
    #print pix_length
    
    BB_SW = (x_min, y_min)
    BB_NW = (x_min, y_min + pix_length * y_pix)
    BB_NE = (x_min + x_length, y_min + pix_length * y_pix)
    BB_SE = (x_min + x_length, y_min)
    
    
    BB_points = np.array((BB_SW, BB_SE, BB_NE, BB_NW))
    #print BB_points
    angle = -np.deg2rad(rotation)
    
    BB_points = Rotate2D(BB_points,BB_SW,ang=angle)
    #print BB_points
    
    #for point in BB_points:
        #point[0], point[1] = XY_To_LL(point[0], point[1])
    '''
    #uses md5 hash of file to decide filename
    #(should prevent duplicates & also stop old kml's from failing when field updated)
    file_hash = md5_from_filename(filename)
    #keyname = job + '/'  + ''.join(random.choice(string.hexdigits) for n in xrange(30)) + '.' + os.path.basename(filename).split('.')[-1]
    keyname = job + '/' + str(file_hash) + '.' + os.path.basename(filename).split('.')[-1]
    m_keyname = job + '/mobile/' + str(file_hash) + '.' + os.path.basename(filename).split('.')[-1]
    bucket = conn.get_bucket('kml.gsb.carteasyn.com')

    #Checks if real key is already online
    if not bucket.get_key(keyname):
        key = bucket.new_key(keyname)
        key.set_contents_from_filename(filename)
        key.set_metadata('Content-Type', 'image/png')
        key.make_public()
        
    #Checks if mobile key is already online
    if not bucket.get_key(m_keyname):
        key = bucket.new_key(m_keyname)
        key.set_contents_from_filename(m_filename)
        key.set_metadata('Content-Type', 'image/png')
        key.make_public()
    
    webname = 'http://{host}/{key}'.format(
        host='kml.gsb.carteasyn.com',
        key=keyname)
        
    m_webname = 'http://{host}/{key}'.format(
        host='kml.gsb.carteasyn.com',
        key=m_keyname)
        
    print webname
    
    
    ground = folder.newgroundoverlay(name=layer)
    m_ground = m_folder.newgroundoverlay(name=layer)
    
    ground.icon.href = webname
    m_ground.icon.href = m_webname
    ground.gxlatlonquad.coords = BB_points
    m_ground.gxlatlonquad.coords = BB_points
    
    
    kml_name = job + '.kmz'
    m_kml_name = job + '_mobile.kmz'
    '''
    print angle
    print np.rad2deg(angle)
    outputfile = filename.split('.')[0]+'.geo.tif'
    
    image_obj = image_obj.rotate(np.rad2deg(angle),resample=Image.BILINEAR,expand=True)
    image_obj = image_obj.convert("RGBA")
    
    backimg = Image.new("RGBA", image_obj.size, (0,0,0,0))
    image_obj = Image.composite(image_obj.convert("RGBA"), backimg, image_obj)
    
    image_obj.save(filename.split('.')[0]+'rotated.png')
    
    sourcefile = (filename.split('.')[0]+'rotated.png')
    destfile = (filename.split('.')[0]+'.geo.tif')
    
    min_y = min((BB_points[0][1],BB_points[1][1],BB_points[2][1],BB_points[3][1]))
    max_y = max((BB_points[0][1],BB_points[1][1],BB_points[2][1],BB_points[3][1]))
    
    min_x = min((BB_points[0][0],BB_points[1][0],BB_points[2][0],BB_points[3][0]))
    max_x = max((BB_points[0][0],BB_points[1][0],BB_points[2][0],BB_points[3][0]))
    
    string ='gdal_translate -a_nodata 0 -a_ullr  %.5f %.5f %.5f %.5f -a_srs EPSG:27700 -of GTiff %s %s' %(min_x,max_y,max_x,min_y,sourcefile,destfile)

    #string = "C:/OSGeo4W64/bin/gdal_translate.exe -of GTiff -a_ullr %s %s %s %s %s %s"%(str(min_x),str(max_y),str(max_x),str(min_y),sourcefile,destfile) 
    print ' '    
    print string
    print ' '
    os.system(string)
    geotif_f = (filename.split('.')[0]+'.TFWgeo.tif')
    string = 'gdal_translate -co "TFW=YES" %s %s' %(destfile, geotif_f)
    os.system(string)
    
    #print np.shape(BB_points)
    #print BB_points[:,0]
    bb_x = np.concatenate((bb_x,BB_points[:,0]))
    bb_y = np.concatenate((bb_y,BB_points[:,1]))
    #bb_x.append(BB_points[:,0])
    #bb_y.append(BB_points[:,1])
        
    GDal_merge_string = GDal_merge_string + ' ' + destfile
#print bb_x
#print bb_y

mean_x = np.mean((min(bb_x), max(bb_x)))
mean_y = np.mean((min(bb_y), max(bb_y)))
'''
ground.lookat.gxaltitudemode = simplekml.GxAltitudeMode.relativetoseafloor
ground.lookat.latitude = mean_x
ground.lookat.longitude = mean_y
ground.lookat.tilt = 90

m_ground.lookat.gxaltitudemode = simplekml.GxAltitudeMode.relativetoseafloor
m_ground.lookat.latitude = mean_x
m_ground.lookat.longitude = mean_y
m_ground.lookat.tilt = 90


kml.savekmz(kml_name)
m_kml.savekmz(m_kml_name)
'''
if os.path.isfile(job + '.geo.tif'):
    os.remove(job + '.geo.tif')
    
#string ='gdalbuildvrt -srcnodata 247 %s %s'%(job + '.geo.vrt',GDal_merge_string)
string ='C:/OSGeo4W64/bin/gdal_merge.py -n 0  -o %s %s' %(job + '.geo.tif',GDal_merge_string)
#string = 'gdalwarp -multi -dstalpha -srcnodata  "247" --config GDAL_CACHEMAX 3000 -wm 3000 %s %s -overwrite' %(GDal_merge_string, job + '.geo.tif')
print string
os.system(string)

string ='C:/OSGeo4W64/bin/gdal2tiles.py -r antialias -s EPSG:27700  %s'%(job + '.geo.tif')
print string
os.system(string)