#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 11:19:54 2020

@author: duttar

Plots all the results of ISCE filterred wrapped interfrograms from Sentinel stack
processing. 
output - stack1.pdf ... in figures folder
Edit it according to number of IFGs

Also plots single unfiltered wrapped ifgs to the figures folder 
"""

from shutil import copyfile
from osgeo import gdal            ## GDAL support for reading virtual files
import os                         ## To create and remove directories
import matplotlib.pyplot as plt   ## For plotting
import numpy as np                ## Matrix calculations
import glob                       ## Retrieving list of files
import argparse

from plotIFG_isce import plotEPGFZdata, plotcomplexdata

parser = argparse.ArgumentParser(description='Plots results of ISCE filterred wrapped interfrograms from Sentinel stack processing.')
parser.add_argument('-i', '--input', type=str, metavar='', required=True, help='Date list of IFGs')

args = parser.parse_args()

#f = open("all_igrams.txt", "r")
f = open(args.input, "r") 


for x in f:
    filename = 'interferograms/' + x[0:17] + '/fine.int.vrt'
    outfile = 'figures/' + x[0:17] + '.png'
    #outfile = 'figures_EPGFZ/' + x[0:17] + '.png'
    #plotcomplexdata(filename, outfile, title = "MERGED IFG ", aspect = 3, datamin = 0, datamax = 10000, draw_colorbar = True)
    plotEPGFZdata(filename, outfile, title = "MERGED IFG ", aspect = 3, datamin = 0, datamax = 10000, draw_colorbar = True)


