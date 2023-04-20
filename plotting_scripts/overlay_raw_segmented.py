import os
import sys
import img3
import argparse
import matplotlib.pyplot as plt
import numpy as np
from numpy.ma import masked_array
from matplotlib import cm

parser = argparse.ArgumentParser()
parser.add_argument('-s', type=str, required=True, help="segmented, nrrd")
parser.add_argument('-r', type=str, required=True, help="raw, nrrd")
parser.add_argument('-id', type=str, required=True, help="sample ID")
args = parser.parse_args()

# load
vmax0 = 6000

if args.id == "340258_2LD_5":
    zslice = 1300
    #vmax = 1300
    vmax = 1500
if args.id == "454371_17_LD_7":
    zslice = 1156
    vmax = 2693 #2200
if args.id == "840258_3_LD_6":
    zslice = 1100
    #vmax = 1700
    vmax = 1300

if args.id == "840295_40_HD_27":
    zslice = 800
    vmax0 = 10000
    #vmax = 2500
    vmax = 2100
if args.id == "340299_35_22_HD":
    zslice = 1000
    vmax0 = 10000
    vmax = 1800
if args.id == "840295_42_HD":
    zslice = 800
    vmax0 = 10000
    #vmax = 1700
    vmax = 1400

if args.id == "840298_16_P_17":
    zslice = 1000
    vmax0 = 6000
    #vmax = 2000
    vmax = 1900
if args.id == "840298_50_P_19":
    zslice = 1000
    vmax0 = 8000
    #vmax = 2000
    vmax = 1200
if args.id == "840298_52_P_20":
    zslice = 1000
    vmax0 = 8000
    #vmax = 1600 #black
    vmax = 2000 #white




raw = img3.nrrd_data(args.r)[:,:,zslice]
raw_maksed = masked_array(raw,raw<100)

seg = img3.nrrd_data(args.s)[:,:,zslice]
seg_masked = masked_array(seg,seg==0)
seg_adj = seg_masked * raw


# plots

# OVERLAY OF RAW AND SEGMENTED
if 1:
    # my_displays_ppi = 108.79  # Dell at USZ
    my_displays_ppi = 98.44  # Apple Cinema HD Display
    NY = np.shape(raw)[0]
    NX = np.shape(raw)[1]
    fig,ax = plt.subplots(1,1,  figsize=(NX/my_displays_ppi, NY/my_displays_ppi),  dpi=my_displays_ppi)

    ax.imshow(raw_maksed.T, interpolation='nearest', cmap=cm.Greys, vmin=0, vmax=vmax, alpha=0.95)
    ax.imshow(seg_masked.T, interpolation='nearest', cmap=cm.cool, vmin=-2e6, vmax=-1e6, alpha=0.95)

    ax.set_axis_off()
    ax.set_facecolor("white")
    plt.savefig("new_pic_overlay_raw_segmented_%s.png" % (args.id), bbox_inches='tight', pad_inches=0, transparent=False)
    plt.close()


# RAW SEPARATELY FROM SEGMENTED
if 0:
    # raw
    fig,ax = plt.subplots(1,1)
    ax.imshow(raw_maksed.T, interpolation='nearest', cmap=cm.Greys, vmin=0, vmax=vmax)
    ax.set_axis_off()
    ax.set_facecolor("white")
    plt.savefig("pic_raw_%s.png" % (args.id), bbox_inches='tight', pad_inches=0, transparent=False)
    plt.close()

    # segmented
    fig,ax = plt.subplots(1,1)
    ax.imshow(seg_masked.T, interpolation='nearest', cmap=cm.Greys, vmin=-2e6, vmax=-1e6)
    ax.set_axis_off()
    ax.set_facecolor("white")
    plt.savefig("pic_seg_%s.png" % (args.id), bbox_inches='tight', pad_inches=0, transparent=False)
    plt.close()


