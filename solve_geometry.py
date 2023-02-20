import os 
from osgeo import gdal
import matplotlib.pyplot as plt
import numpy as np
import h5py

def gdal_open(fname, returnProj=False, userNDV=None):
    if os.path.exists(fname + '.vrt'):
        fname = fname + '.vrt'
    try:
        ds = gdal.Open(fname, gdal.GA_ReadOnly)
    except:
        raise OSError('File {} could not be opened'.format(fname))
    proj = ds.GetProjection()
    gt = ds.GetGeoTransform()

    val = []
    for band in range(ds.RasterCount):
        b = ds.GetRasterBand(band + 1)  # gdal counts from 1, not 0
        data = b.ReadAsArray()
        if userNDV is not None:
            logger.debug('Using user-supplied NoDataValue')
            data[data == userNDV] = np.nan
        else:
            try:
                ndv = b.GetNoDataValue()
                data[data == ndv] = np.nan
            except:
                logger.debug('NoDataValue attempt failed*******')
        val.append(data)
        b = None
    ds = None

    if len(val) > 1:
        data = np.stack(val)
    else:
        data = val[0]

    if not returnProj:
        return data
    else:
        return data, proj, gt


los = gdal_open('los.rdr')
lon = gdal_open('lon.rdr')
lat = gdal_open('lat.rdr')

print('los_rdr.shape: '+str(len(los[0])) + ', ' + str(len(los[1])))

incidence = los[0,:]
heading = los[1,:]

def sind(theta):
    return np.sin(np.radians(theta))

def cosd(theta):
    return np.cos(np.radians(theta))

east = sind(incidence) * cosd(heading + 90)
north = sind(incidence) * sind(heading + 90)
up = cosd(incidence)

print('length of ENU: ' + str(len(east)) + ', ' + str(len(north)) + ', ' + str(len(up)))

# save to new hdf5 file
with h5py.File('geometry.h5', 'w') as hf:
    hf.create_dataset("lon",  data = lon)
    hf.create_dataset("lat",  data = lat)
    hf.create_dataset("incidence",  data = incidence)
    hf.create_dataset('heading', data = heading)
    hf.create_dataset('east', data = east)
    hf.create_dataset('north', data = north)
    hf.create_dataset('up', data = up)
    hf.close()
