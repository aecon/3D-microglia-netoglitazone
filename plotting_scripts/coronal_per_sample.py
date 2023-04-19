import os
import sys
import adv
import argparse
import matplotlib.pyplot as plt
import numpy as np
import skimage.io
from numpy.ma import masked_array
from matplotlib import cm

def coronal(ax, Nc, slices, cells_masked, normal, cmap, Vmax, Vmin, outfile):

    # load atlas
    fatlas="/media/athena-admin/FastSSD1/Athena/atlas/ABA_25um_reference.tif"
    atlas0 = skimage.io.imread(fatlas, plugin='tifffile').T
    atlas = np.zeros(np.shape(cells_masked))
    atlas[:,:,:] = atlas0[:, :, 0:np.shape(cells_masked)[2]]

    # plot coronal slices
    for ic in range(Nc):
        i = slices[ic]
        pa = ax[ic].imshow(atlas[:,i,:], interpolation='nearest', cmap=cm.gray)

        if normal !=0:
            alphas = ((cells_masked[:,i,:]))/normal; alphas[alphas<0.1]=0.1; alphas[alphas>1]=1
        else:
            alphas = 1
        pb = ax[ic].imshow(cells_masked[:,i,:], interpolation='nearest', cmap=cmap, alpha=alphas, vmin=Vmin, vmax=Vmax)

        ax[ic].set_axis_off()
        ax[ic].set_facecolor("white")

#        if ic==0:
#            ax[ic].annotate(text="%s"%args.s, xy=(16, 36), xycoords='data', color='w', fontsize=8)

    plt.subplots_adjust(wspace=0, hspace=0)
    plt.savefig(outfile, bbox_inches='tight', pad_inches=0, transparent=False)
    plt.close()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, required=True, help="input: voxelized.tif")
    parser.add_argument('-o', type=str, required=True, help="output folder")
    parser.add_argument('-s', type=str, required=True, help="sample ID")
    args = parser.parse_args()


    sample = args.s
    print(sample)
    color = 'm'
    vmin=-2e6; vmax=-1e6
    cmap = cm.cool

    # load
    cells = skimage.io.imread(args.i, plugin='tifffile').T
    cells_masked = masked_array(cells,cells==0)

    # plot
    Nc=8
    Nr=1
    slices = [50, 100, 150, 200, 250, 300, 350, 400]
    fig,ax = plt.subplots(Nr,Nc, figsize=(16,3), facecolor='black')
    outfile = "%s/pic_density_coronal_%s.pdf" % (args.o, sample)
    normal = 4500
    coronal(ax, Nc, slices, cells_masked, normal, cmap, vmax, vmin, outfile)

