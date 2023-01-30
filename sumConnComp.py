import os
from osgeo import gdal
import numpy as np
import scipy.io as sio


sumdata = np.zeros([7520, 7509])

## plot all IFGs
# IFG_list = sorted(os.listdir())
# IFG_list = IFG_list[0:464] # remove sumConnComp.ipynb, only keep the date
# for i in range(int(len(IFG_list))):
#     filename = IFG_list[i] + '/filt_fine.unw.conncomp.vrt'
#     ds = gdal.Open(filename, gdal.GA_ReadOnly)
#     data = ds.GetRasterBand(1).ReadAsArray()
#     ds = None
#     data[data>0] = 1
#     #sumdata = np.concatenate((sumdata, data), axis =1)
#     #sumdata[i, :, :] = data
#     sumdata += data

## plot exclude IFGs
# f = open('../excludeIfgDate.txt', "r") 
# for i in f:
#     filename = i[0:17] + '/filt_fine.unw.conncomp.vrt'
#     ds = gdal.Open(filename, gdal.GA_ReadOnly)
#     data = ds.GetRasterBand(1).ReadAsArray()
#     ds = None
#     data[data>0] = 1
#     #sumdata = np.concatenate((sumdata, data), axis =1)
#     #sumdata[i, :, :] = data
#     sumdata += data

## plot keep IFGs
f = open('../keepIfgDate.txt', "r") 
for i in f:
    filename = i[0:17] + '/filt_fine.unw.conncomp.vrt'
    ds = gdal.Open(filename, gdal.GA_ReadOnly)
    data = ds.GetRasterBand(1).ReadAsArray()
    ds = None
    data[data>0] = 1
    #sumdata = np.concatenate((sumdata, data), axis =1)
    #sumdata[i, :, :] = data
    sumdata += data


sum2 = sumdata/np.max(sumdata) # normalized 

print('Max value for sumdata: ', np.max(sumdata))
print('Max value for normalized sumdata: ', np.max(sum2))
print('Index of max value:', np.unravel_index(np.argmax(sumdata, axis = None), sumdata.shape))

varname1 = 'sumConnComp_keep.mat'
sio.savemat(varname1, {'sum':sumdata, 'sum_normalized': sum2})
