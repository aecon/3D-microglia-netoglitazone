import os
import sys
import adv
import argparse
import matplotlib.pyplot as plt
import numpy as np
import skimage.io
from numpy.ma import masked_array
from matplotlib import cm
from matplotlib import colors
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable

import statsmodels.stats.multitest as multi

parser = argparse.ArgumentParser()
parser.add_argument('-f1', type=str, required=True, help="average file 1: cells_average_groupX.nrrd")
parser.add_argument('-f2', type=str, required=True, help="average saline: cells_average_groupX.nrrd")
parser.add_argument('-f1s', type=str, required=True, help="std file 1: std_cells_average_groupX.nrrd")
parser.add_argument('-f2s', type=str, required=True, help="std saline: std_cells_average_groupX.nrrd")
parser.add_argument('-R', type=int, required=True, help="blur radius")
parser.add_argument('-g', type=int, required=True, help="1 or 2")
parser.add_argument('-o', type=str, required=True, help="outdir")
parser.add_argument('-a', type=str, default="/media/athena-admin/FastSSD1/Athena/atlas/ABA_25um_reference.tif", help="atlas file")
parser.add_argument('-aa', type=str, default="/media/athena-admin/FastSSD1/Athena/atlas/ABA_25um_annotation.tif", help="atlas file for interior (>0)")
args = parser.parse_args()


fatlas = args.a
atlas  = skimage.io.imread(fatlas, plugin='tifffile').T


colors_magenta = [(1, 0, 1), (1, 0, 1)]  # Magenta
colors_green   = [(0, 1, 0), (0, 1, 0)]  # Green
cmap_name = 'my_cmap'
cmap_green = LinearSegmentedColormap.from_list(cmap_name, colors_green, N=100)
cmap_magenta = LinearSegmentedColormap.from_list(cmap_name, colors_magenta, N=100)


# Normalization
print("Using data for R =" , args.R)
if args.R==3:
    norm=200000
elif args.R==7:
    norm=40000
elif args.R==15:
    norm=200000
else:
    print("R value not supported")
    sys.exit()


# load per-voxel means
fcells1 = args.f1
fcells2 = args.f2
cells1 = adv.nrrd_data(fcells1)/norm
cells2 = adv.nrrd_data(fcells2)/norm
#print("means 1:", np.min(cells1), np.max(cells1))
#print("means 2:", np.min(cells2), np.max(cells2))


# load per-voxel stds
fcells1s = args.f1s
fcells2s = args.f2s
cells1s = adv.nrrd_data(fcells1s)/norm
cells2s = adv.nrrd_data(fcells2s)/norm
#print("stds 1:", np.min(cells1s), np.max(cells1s))
#print("stds 2:", np.min(cells2s), np.max(cells2s))


# two-sided t-test pvalue
from scipy.stats import ttest_ind_from_stats
ttest = ttest_ind_from_stats(mean1=cells1, std1=cells1s, nobs1=3,
                             mean2=cells2, std2=cells2s, nobs2=3)


# find non-nan pvalues
condition = ((ttest.pvalue>0)*(ttest.pvalue<1)) == 1
statistic = np.where( condition , ttest.statistic, 0)
pvalues   = np.where( condition , ttest.pvalue,    0)


# split effect
positive_pv = np.where(statistic>0, pvalues, 0)
negative_pv = np.where(statistic<0, pvalues, 0)


# write pvalues
group = args.g; #print(group)

# -- positive effect
name_raw = "%s/../processed_R%d/pv_cells_group%d_pos.raw"%(args.o, args.R, group)
name_nrrd = "%s/../processed_R%d/pv_cells_group%d_pos.nrrd"%(args.o, args.R, group)
o = adv.mmap_create(name_raw, np.dtype("float"), np.shape(pvalues))
adv.nrrd_write(name_nrrd, name_raw, o.dtype, o.shape, (1,1,1))
o[:,:,:] = positive_pv[:,:,:]

# -- negative effect
name_raw = "%s/../processed_R%d/pv_cells_group%d_neg.raw"%(args.o, args.R, group)
name_nrrd = "%s/../processed_R%d/pv_cells_group%d_neg.nrrd"%(args.o, args.R, group)
o = adv.mmap_create(name_raw, np.dtype("float"), np.shape(pvalues))
adv.nrrd_write(name_nrrd, name_raw, o.dtype, o.shape, (1,1,1))
o[:,:,:] = negative_pv[:,:,:]

