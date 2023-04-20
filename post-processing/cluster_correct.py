import os
import glob
import numpy as np
import scipy.ndimage.measurements as sm
import argparse
import tifffile
import img3
import skimage.io


parser = argparse.ArgumentParser()
parser.add_argument('-p', type=str, required=True, help="uncorrected pvalues, nrrd")
args = parser.parse_args()


# pvalue cluster correction options
pval_thresh = 0.05
size_pct = 95

# montage options
Nc = 6
Nr = 5


def reorder4montage(array_):

    array = array_[:,:,20::]
    Nbatch = (np.shape(array)[2] // (Nr*Nc))
    newa = np.zeros( [np.shape(array)[0], np.shape(array)[1], Nc*Nr] )
    l = 0
    for j in range(Nr):
        for i in range(Nc):
            k = (j + i*Nr) * Nbatch
            newa[:,:,l] = array[:,:,k]
            l = l+1
            print(l, k)
    return newa


def store4montage(name_raw, name_nrrd, array):
    shape = np.shape(array)
    shape_rot = (shape[2], shape[0], shape[1])

    o = img3.mmap_create(name_raw, np.dtype("float"), (shape_rot[0], shape_rot[1], Nc*Nr) )
    img3.nrrd_write(name_nrrd, name_raw, o.dtype, o.shape, (1,1,1))
    tmp_ = sag2cor(array)
    o[:,:,:] = reorder4montage(tmp_)


def sag2cor(array):
    tmp = np.rot90(array, k=1, axes=(0, 2))
    tmp1 = np.rot90(tmp, k=-1, axes=(1, 2))
    tmp2 = tmp1[:,:,::-1]
    return tmp2


def filter_sizes_below_pct(mask, pct = 95, csize_thresh = None):
    imglabel, nlab = sm.label(mask)  # connected components. returns: labels, Nobj
    labels = np.arange(0, nlab+1)
    csize = sm.sum(np.ones(imglabel.shape), labels = imglabel, index = labels) # vol. per connected comp.
    csize[0] = 0
    if csize_thresh is None:
        csize_thresh = np.percentile(csize, pct)
    uniq, uniq_idx, uniq_inv, uniq_cnts = np.unique(imglabel, return_index = True, return_inverse = True, return_counts = True)
    assert(np.array_equal(uniq, labels))
    imgsize = np.where(csize >= csize_thresh, csize, 0)[uniq_inv].reshape(imglabel.shape)
    return imgsize


# pvalue cluster correction
pvalues = img3.nrrd_data(args.p)
pvalues_thresh = np.where(pvalues <= pval_thresh, 1, 0) # binarization of pvalues
pvalues_corr_sizes = filter_sizes_below_pct(pvalues_thresh, csize_thresh = size_pct)
pvalues_corr = np.where(pvalues_corr_sizes > 0, pvalues, 0)

# mask pixels outside atlas
from numpy.ma import masked_array
fatlas="/media/athena-admin/FastSSD1/Athena/atlas/ABA_25um_distance_to_surface.tif"
atlas0 = skimage.io.imread(fatlas, plugin='tifffile').T
atlas = np.zeros(np.shape(pvalues_corr))
atlas[:,:,:] = atlas0[:, :, 0:np.shape(pvalues_corr)[2]]
cells_masked = masked_array(pvalues_corr, np.logical_or(pvalues_corr==0, atlas==0) )
pvalues_corr[atlas==0] = 0

# store corrected pvalues
input_file = args.p
outfile = input_file.replace('.nrrd', '_corrected.tif')
name_raw  = input_file.replace('.nrrd', '_corrected.raw')
name_nrrd = input_file.replace('.nrrd', '_corrected.nrrd')
store4montage(name_raw, name_nrrd, pvalues_corr)

# store atlas
fatlas=("/media/athena-admin/FastSSD1/Athena/atlas/ABA_25um_reference.tif")
atlas_ = skimage.io.imread(fatlas, plugin='tifffile').T
atlas = np.zeros(np.shape(pvalues_corr))
atlas[:,:,:] = atlas_[:, :, 0:np.shape(pvalues_corr)[2]]
name_raw  = "%s/atlas_rot.raw"  % (os.path.dirname(input_file))
name_nrrd = "%s/atlas_rot.nrrd" % (os.path.dirname(input_file))
store4montage(name_raw, name_nrrd, atlas)



# plot
# import matplotlib.pyplot as plt
# from matplotlib import cm
# from coronal_per_sample import coronal
# Nc=8
# Nr=1
# slices = [50, 100, 150, 200, 250, 300, 350, 400]
# fig,ax = plt.subplots(Nr,Nc, figsize=(16,3), facecolor='black')
# 
# 
# coronal(ax, Nc, slices, cells_masked, 0, cm.get_cmap('inferno_r'), 0.05, 0, outfile.replace('.tif', '.pdf') )

