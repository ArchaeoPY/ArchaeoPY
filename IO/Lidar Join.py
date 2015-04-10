import glob, os
import image_slicer
from PIL import Image

####-----####
#Tiles Directory
t_dir = 'C:/Users/fpopecarter/Documents/GitHub/Data/Tiles'

#Tile Prefix
t_pref = 'lidar'

#Tile extension
t_ext = '.png'
####-----####

#makes list of all 'tiles' matching pattern
tile_names = glob.glob(t_dir + '/' + t_pref + '*' + t_ext)

#calculates desired size of total data
name, rows, columns = os.path.basename(tile_names[-1]).split('.')[0].split('_')
im_dimen = Image.open(tile_names[0]).size
comb_dimen=  (int(im_dimen[0])*int(columns),int(im_dimen[1])*int(rows))

#Creates new blank image to paste tiles into
comb = Image.new('RGBA', comb_dimen, None)

#iterates through tiles and pastes them into right coordinate
for tilen in tile_names:
    name, row, column = os.path.basename(tilen).split('.')[0].split('_')
    coords = (int(column)-1) * int(im_dimen[0]), (int(row)-1) * int(im_dimen[1])
    im = Image.open(tilen)
    comb.paste(im, coords)
    
#saves data
#this takes a while..
comb.save(t_dir + t_pref + t_ext)
    