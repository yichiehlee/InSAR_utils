# load library
import os
import numpy as np
import h5py
import argparse

parser = argparse.ArgumentParser(description='Convert velocity.h5 to velocity.mat')
parser.add_argument('-o', '--output', type=str, metavar='', required=True, help='Output File Name. e.g. AT04_geo_velocity.mat ')
args = parser.parse_args()

#load velocity
with h5py.File('geo/geo_velocity.h5', "r") as f:
    velocity = f['velocity'][()]

#load geometry
radar_file = h5py.File('geo/geo_geometryRadar.h5','r')

lat = radar_file['latitude'][()]
lon = radar_file['longitude'][()]

from scipy.io import savemat
savemat(args.output, {'geo_velocity': velocity, 'lat': lat, 'lon': lon})
