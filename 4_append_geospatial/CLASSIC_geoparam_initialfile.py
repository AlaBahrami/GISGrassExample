# -*- coding: utf-8 -*-
"""
Created on Wed May  3 14:45:42 2023

Purpose: The purpose of this script is to read a domain grid cells and read a 
shape file which contains grid geospatial information. Also read the mapped slope file 
and append it to the initial file. 

Programmer: AlaBahrami

See also:  

last modified : 05/09/2023
                1) write geophysical parameters to initial netcdf file  

                2) convert SLOPE and DD arrary to 3D to match the structure of
                   inital condition files array 
                   
                10/12/2023   
                Modified the inital condition file to include GRKF and WFCI in 
                the initial condition file.
                
"""
#%% import modules 
import xarray as xs 
import pandas as pd 
import geopandas as gpd
import numpy as np 

#%% define input/output files 
grid_shape      = '/scratch/baha2501/GRASS_example/input/shape/Global_CLASSIC_grid.shp'
grid_shape_edit = '/scratch/baha2501/GRASS_example/input/shape/Global_CLASSIC_grid_edit.shp'
slope_data      = '/scratch/baha2501/GRASS_example/output/Glob_CLASSIC_slope.csv' 
init_file       = '/scratch/baha2501/GRASS_example/input/Initial/global/rsFile_1degree_global.nc'
init_file_edit  = '/scratch/baha2501/GRASS_example/input/Initial/global/rsFile_1degree_global_edit.nc'

#%% read the initial file and dimension variables 
data = xs.open_dataset(init_file)
lat  = data['lat']
lon  = data['lon']
tile = data['tile']

#%% read the shapefiles, sort values if they are not sorted, and calculate the drainage density   
grid  = gpd.read_file(grid_shape)
grid  = grid.sort_values(by =['ID_s'])
grid.reset_index(drop=True, inplace=True)

# reading calculated slope [degree]
slope  = pd.read_csv(slope_data)
slope  = slope.sort_values(by =['IDs'])
slope.reset_index(drop=True, inplace=True)

#%% Append the geophysical parameters to grid shape file  
# present the tan value of slope instead of angle 
grid['Slope']           = np.tan(slope['averaged_slope_degrees'].values * np.pi/180)

#%% reshape geophysical parameters to a 2D grid 
# NB2: the reason I used the padding is that easymore clips the boundary domain 
# of interest one column from each side and top and bottom. 
# so I pad it to be consistent with the original initial condition file. 
# I have to subtract the constact 2 to reduce the size of lat and lon matrices.  
slope = np.reshape(grid['Slope'].values, (len(lat)-2, len(lon)-2))

# padding the slope matriz  
slope = np.pad(slope, 1, mode='constant', constant_values=np.nan) 

# convert the DD tp 3D to match the structure of other variables 
slope = slope[np.newaxis, :, :]

#%% append geophysical parameters to the intial condition file 
# the value of DD is based on a forest GRU in MESH, but it can be calcaulated based
# on global river network 
DD = np.ones(len(lat)*len(lon)) * 4.000/1000          # DD [m/m2] convert from km/km2 to m/m2
DD = np.reshape(DD, (len(lat), len(lon)))
# convert it to 3D array 
DD    = DD[np.newaxis, :, :]

# the value of GRFK is based on a forest GRU in MESH 
GRKF = np.ones(len(lat)*len(lon)) * 0.1          # GRKF [-]  
GRKF = np.reshape(GRKF, (len(lat), len(lon)))
# convert it to 3D array 
GRKF    = GRKF[np.newaxis, :, :]

# the value of GRFK is based on a forest GRU in MESH 
WFCI = np.ones(len(lat)*len(lon)) * 0.05          # WFCI [m s^-1]  
WFCI = np.reshape(WFCI, (len(lat), len(lon)))
# convert it to 3D array 
WFCI    = WFCI[np.newaxis, :, :]

# the value of GRFK is based on a forest GRU in MESH 
MANN = np.ones(len(lat)*len(lon)) * 0.242          # MANN [-]  
MANN = np.reshape(MANN, (len(lat), len(lon)))
# convert it to 3D array 
MANN    = MANN[np.newaxis, :, :]

data['XSLOPE'] = xs.DataArray(
    slope, coords=[tile, lat, lon], dims=('tile','lat', 'lon')).astype(np.float32)

data['DD'] = xs.DataArray(
    DD, coords=[tile, lat, lon], dims=('tile','lat', 'lon')).astype(np.float32)

data['GRKF'] = xs.DataArray(
    GRKF, coords=[tile, lat, lon], dims=('tile','lat', 'lon')).astype(np.float32)

data['WFCI'] = xs.DataArray(
    WFCI, coords=[tile, lat, lon], dims=('tile','lat', 'lon')).astype(np.float32)

data['MANN'] = xs.DataArray(
    MANN, coords=[tile, lat, lon], dims=('tile','lat', 'lon')).astype(np.float32)

#%% save modified initial file and grid shape file 
data.to_netcdf(init_file_edit)
grid.to_file(grid_shape_edit)