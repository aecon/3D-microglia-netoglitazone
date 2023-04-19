import os
import argparse
import skimage.io
import numpy as np
import pandas as pd
import adv

fatlas_D = "/media/athena-admin/FastSSD1/Athena/atlas/ABA_25um_distance_to_surface.tif"
fatlas_A = "/media/athena-admin/FastSSD1/Athena/atlas/ABA_25um_annotation.tif"
fregions = "atlas.tab"


def load_atlas(f):
    a = skimage.io.imread(f, plugin='tifffile').T
    return a


def load_atlas_cropped(f, x):
    """
    Assumes that sample is cropped in the Z-direction
    """
    a_ = load_atlas(f)
    a = np.zeros(np.shape(x))
    a[:,:,:] = a_[:, :, 0:np.shape(x)[2]]
    return a


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str, nargs='+', required=True, help="cells, tiff")
    args = parser.parse_args()

    for fcells in args.f:

        print(fcells)

        fw = open("%s/volume_per_region.dat" % (os.path.dirname(fcells)), 'w')
        fw.write("%15s %15s\n" % ("Region ID", "Cell volume"))

        # load cells
        cells = skimage.io.imread(fcells, plugin='tifffile').T

        # load annotated regions
        atlas = load_atlas_cropped(fatlas_A, cells)
        regions = pd.read_csv(fregions, header=None, sep='\t', lineterminator='\n')

        # exclude stuff outside atlas
        atlas_D = load_atlas_cropped(fatlas_D, cells)
        cells[atlas_D==0] = 0

        # (cell) volume per region
        vol_regions = np.zeros(len(regions))
        vol_cells = np.zeros(len(regions))

        # loop over all regions
        ids = regions.loc[:,0]
        names = regions.loc[:,3]

        if fcells==args.f[0]:
            fr = open("regions_info.dat", 'w')
            fr.write("%15s %15s\n" % ("Region ID", "Region volume"))

        for i,ID in enumerate(ids):
            idx = np.where(atlas==ID)
            vol_regions[i] = np.shape(idx)[1]
            vol_cells[i] = np.sum(cells[idx])
            print(i, vol_cells[i])
            fw.write("%15d %15g\n" % (i, vol_cells[i]))

            if fcells==args.f[0]:
                fr.write("%15d %15d\n" % (i, vol_regions[i]))

        fw.close()

        if fcells==args.f[0]:
            fr.close()


