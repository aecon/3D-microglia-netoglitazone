import os
import sys
import argparse
import matplotlib.pyplot as plt
import numpy as np
import skimage.io
from numpy.ma import masked_array
from matplotlib import cm
from matplotlib import colors
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable


# Files
fshort_lc = "/media/athena-admin/FastSSD1/Athena/francesca_202203/plaques_processed/wren_short_cohort/size_corrected_maps/Placebo vs Low Dose (total size).tif"
fshort_lm = "/media/athena-admin/FastSSD1/Athena/francesca_202203/plaques_processed/wren_short_cohort/size_corrected_maps/Placebo vs Low Dose (mean size).tif"
fshort_hc = "/media/athena-admin/FastSSD1/Athena/francesca_202203/plaques_processed/wren_short_cohort/size_corrected_maps/Placebo vs High Dose (total size).tif"
fshort_hm = "/media/athena-admin/FastSSD1/Athena/francesca_202203/plaques_processed/wren_short_cohort/size_corrected_maps/Placebo vs High Dose (mean size).tif"
flong_lc  = "/media/athena-admin/FastSSD1/Athena/francesca_202203/plaques_processed/wren_long_cohort/size_corrected_maps/Placebo vs Low Dose (total size).tif"
flong_lm  = "/media/athena-admin/FastSSD1/Athena/francesca_202203/plaques_processed/wren_long_cohort/size_corrected_maps/Placebo vs Low Dose (mean size).tif"
flong_hc  = "/media/athena-admin/FastSSD1/Athena/francesca_202203/plaques_processed/wren_long_cohort/size_corrected_maps/Placebo vs High Dose (total size).tif"
flong_hm  = "/media/athena-admin/FastSSD1/Athena/francesca_202203/plaques_processed/wren_long_cohort/size_corrected_maps/Placebo vs High Dose (mean size).tif"


# Load data
short_lc = skimage.io.imread(fshort_lc, plugin='tifffile')
short_lm = skimage.io.imread(fshort_lm, plugin='tifffile')
short_hc = skimage.io.imread(fshort_hc, plugin='tifffile')
short_hm = skimage.io.imread(fshort_hm, plugin='tifffile')
long_lc  = skimage.io.imread(flong_lc,  plugin='tifffile')
long_lm  = skimage.io.imread(flong_lm,  plugin='tifffile')
long_hc  = skimage.io.imread(flong_hc,  plugin='tifffile')
long_hm  = skimage.io.imread(flong_hm,  plugin='tifffile')
print(np.shape(long_hm))


# Project along z
pshort_lc = np.sum(short_lc, axis=0 )
pshort_lm = np.sum(short_lm, axis=0 )
pshort_hc = np.sum(short_hc, axis=0 )
pshort_hm = np.sum(short_hm, axis=0 )
plong_lc  = np.sum(long_lc , axis=0 )
plong_lm  = np.sum(long_lm , axis=0 )
plong_hc  = np.sum(long_hc , axis=0 )
plong_hm  = np.sum(long_hm , axis=0 )
print(np.shape(plong_hm))


# Collect data in lists
data = [pshort_lc, pshort_lm, pshort_hc, pshort_hm, plong_lc, plong_lm, plong_hc, plong_hm]
names =["short_low_count", "short_low_mean", "short_high_count", "short_high_mean", "long_low_count", "long_low_mean", "long_high_count", "long_high_mean"]


# Reverse summed pvalues (values anw dont mean anything anymore!)
# shape: (320, 456, 3)
# z[0] -> atlas
for d in data:

    for ii in [1,2]:
        c = d[:,:,ii]
        idx = c>0
        c[idx] = 1.0 + np.log10(1.0/c[idx])   # significant pixels will have higher value. 0 stays 0.
        d[:,:,ii] = c[:]

print(np.min(pshort_lc [:,:,1::]))
print(np.min(pshort_lm [:,:,1::]))
print(np.min(pshort_hc [:,:,1::]))
print(np.min(pshort_hm [:,:,1::]))
print(np.min(plong_lc  [:,:,1::]))
print(np.min(plong_lm  [:,:,1::]))
print(np.min(plong_hc  [:,:,1::]))
print(np.min(plong_hm  [:,:,1::]))


# Save projected tiffs
oshort_lc = "/media/athena-admin/FastSSD1/Athena/francesca_202203/plaques_processed/projected_short_Placebo_Low_total.tif"
oshort_lm = "/media/athena-admin/FastSSD1/Athena/francesca_202203/plaques_processed/projected_short_Placebo_Low_mean.tif"
oshort_hc = "/media/athena-admin/FastSSD1/Athena/francesca_202203/plaques_processed/projected_short_Placebo_High_total.tif"
oshort_hm = "/media/athena-admin/FastSSD1/Athena/francesca_202203/plaques_processed/projected_short_Placebo_High_mean.tif"

olong_lc  = "/media/athena-admin/FastSSD1/Athena/francesca_202203/plaques_processed/projected_long_Placebo_Low_total.tif"
olong_lm  = "/media/athena-admin/FastSSD1/Athena/francesca_202203/plaques_processed/projected_long_Placebo_Low_mean.tif"
olong_hc  = "/media/athena-admin/FastSSD1/Athena/francesca_202203/plaques_processed/projected_long_Placebo_High_total.tif"
olong_hm  = "/media/athena-admin/FastSSD1/Athena/francesca_202203/plaques_processed/projected_long_Placebo_High_mean.tif"

skimage.io.imsave(oshort_lc, pshort_lc, plugin='tifffile')
skimage.io.imsave(oshort_lm, pshort_lm, plugin='tifffile')
skimage.io.imsave(oshort_hc, pshort_hc, plugin='tifffile')
skimage.io.imsave(oshort_hm, pshort_hm, plugin='tifffile')

skimage.io.imsave(olong_lc,  plong_lc , plugin='tifffile')
skimage.io.imsave(olong_lm,  plong_lm , plugin='tifffile')
skimage.io.imsave(olong_hc,  plong_hc , plugin='tifffile')
skimage.io.imsave(olong_hm,  plong_hm , plugin='tifffile')


# Plot
k=0
for t,d in zip(names, data):
    Nc=1
    Nr=1
    fig,ax = plt.subplots(Nr,Nc, facecolor='black')

    plt.imshow(d[:,:,0], interpolation='nearest', cmap=cm.gray, vmin=0, vmax=82360)

    m1 = masked_array(d[:,:,1], d[:,:,1]==0)
    plt.imshow(m1, interpolation='nearest', cmap=cm.plasma_r, alpha=0.5, vmin=0, vmax=4)

    m2 = masked_array(d[:,:,2], d[:,:,2]==0)
    plt.imshow(m2, interpolation='nearest', cmap=cm.Blues, alpha=0.5, vmin=0, vmax=4)

    plt.subplots_adjust(wspace=0, hspace=0)
    plt.savefig("img_%s.png" % t, bbox_inches='tight', pad_inches=0, transparent=False)
    plt.close()
    k = k+1


