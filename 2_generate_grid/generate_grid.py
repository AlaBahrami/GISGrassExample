"""
Created on Wed Apr 12 14:47:40 2023

@author: Ala Bahrami 

The purpose of this function is to create a MESH grid based on lat/lon centroids info

Source : https://github.com/ShervanGharari/EASYMORE/blob/23113deebe2128faa189c5d79e2edc218154b0b8/easymore/easymore.py#L745

todo: 1) place for improvement use easymore for generating the source shape file
         instead of using the internal function lat_lon_SHP(), I can call easymore directly  

"""
#%% import modules 
from easymore.easymore import easymore # version 1 and bellow
#from easymore import Easymore
import xarray as xs 
import numpy as np
#%% input file and reading the input lat/lon
## Canada
# init_file       = '/scratch/baha2501/GRASS_example/input/Initial/init_hybrid_v1.2.nc'
# output          = '/scratch/baha2501/GRASS_example/input/shape/Canada_CLASSIC_grid.shp'
## Fraser
#init_file       = '/scratch/baha2501/GRASS_example/input/Initial/init_hybrid_v1.2_masked_fraser_pad.nc'
#output          = '/scratch/baha2501/GRASS_example/input/shape/Fraser_CLASSIC_grid.shp'
## Glob
init_file       = '/scratch/baha2501/GRASS_example/input/Initial/global/rsFile_1degree_global.nc'
output          = '/scratch/baha2501/GRASS_example/input/shape/Global_CLASSIC_grid.shp'
data            = xs.open_dataset(init_file)
lon             = data['lon'].values  # longitude, lon. Check variable name form Initial condition file 
lat             = data['lat'].values  # latitude, lat

#%% construct a 2D array from 1D array of lat/lon
# NB : in case the the lat/lon are 2D this step should be skipped 
lat2D = np.repeat(lat, 360, axis=0)
lat2D = lat2D.reshape(180,360)

lon   = lon -180 # convert the range to be from -180 to 180 
lon2D = np.repeat(lon, 180, axis=0)
lon2D = lon2D.reshape(360,180)
lon2D = lon2D.T

#%% intializing the easymore and create the source shape file and save it 
esmr = easymore() #version 1 and bellow  
#esmr = Easymore() #version 2 and above

shp = esmr.lat_lon_SHP(lat2D,lon2D, file_name = None)

# assining the crs 
shp = shp.set_crs('EPSG:4326')

# save the file 
shp.to_file(output)
