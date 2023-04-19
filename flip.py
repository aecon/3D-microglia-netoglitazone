import os
import sys
import numba
import argparse
import numpy as np
import adv

# Need flipping ("right" brains):
#   454371_17_LD_7
#   840258_3_LD_6


@numba.njit(parallel=True)
def flipx(a, out):
    nx, ny, nz = a.shape
    for k in numba.prange(nz):
        for j in numba.prange(ny):
            for i in numba.prange(nx):
                out[i, j, k] = a[(nx-i-1), j, k]


# Flip only raw
if 1:
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, required=True, help="raw data, nrrd")
    args = parser.parse_args()
    
    raw = adv.nrrd_data(args.i)
    
    odir    = os.path.dirname(args.i)
    basename = os.path.basename(args.i)
    flip_raw = adv.mmap_create("%s/flip_%s.raw" % (odir, basename), raw.dtype, raw.shape)
    adv.nrrd_write("%s/flip_%s.nrrd" % (odir, basename), "%s/flip_%s.raw" % (odir, basename), flip_raw.dtype, flip_raw.shape, (1,1,1))
    
    flipx(raw, flip_raw)


# Flip both segmented cells and raw
if 0:
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, required=True, help="raw data, nrrd")
    parser.add_argument('-c', type=str, required=True, help="cell data, nrrd")
    args = parser.parse_args()
    
    raw = adv.nrrd_data(args.i)
    cells = adv.nrrd_data(args.c)
    
    odir    = os.path.dirname(args.c)
    flip_cells = adv.mmap_create("%s/flip_segmented.raw" % odir, cells.dtype, cells.shape)
    flip_raw = adv.mmap_create("%s/flip_raw.raw" % odir, raw.dtype, raw.shape)
    adv.nrrd_write("%s/flip_segmented.nrrd" % odir, "%s/flip_segmented.raw" % odir, flip_cells.dtype, flip_cells.shape, (1,1,1))
    adv.nrrd_write("%s/flip_raw.nrrd" % odir, "%s/flip_raw.raw" % odir, flip_raw.dtype, flip_raw.shape, (1,1,1))
    
    flipx(raw, flip_raw)
    flipx(cells, flip_cells)

