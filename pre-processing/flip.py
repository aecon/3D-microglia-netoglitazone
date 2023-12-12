import os
import sys
import numba
import argparse
import numpy as np
import img3


@numba.njit(parallel=True)
def flipx(a, out):
    nx, ny, nz = a.shape
    for k in numba.prange(nz):
        for j in numba.prange(ny):
            for i in numba.prange(nx):
                out[i, j, k] = a[(nx-i-1), j, k]

@numba.njit(parallel=True)
def flipz(a, out):
    nx, ny, nz = a.shape
    for k in numba.prange(nz):
        for j in numba.prange(ny):
            for i in numba.prange(nx):
                out[i, j, k] = a[i, j, (nz-k-1)]


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, required=True, help="raw data, nrrd")
    parser.add_argument('-flipX', action='store_true')
    parser.add_argument('-flipZ', action='store_true')
    args = parser.parse_args()

    raw = img3.nrrd_data(args.i)

    odir    = os.path.dirname(args.i)
    basename = os.path.basename(args.i)
    flip_raw = img3.mmap_create("%s/flip_%s.raw" % (odir, basename), raw.dtype, raw.shape)
    tmp = img3.mmap_create("%s/tmp.raw" % (odir), raw.dtype, raw.shape)
    img3.nrrd_write("%s/flip_%s.nrrd" % (odir, basename), "%s/flip_%s.raw" % (odir, basename), flip_raw.dtype, flip_raw.shape, (1,1,1))

    if (args.flipX == False) and (args.flipZ == False):
        print("Error: No flip specified. Please specify either flipX or flipZ or both.")
        sys.exit()

    tmp[:,:,:] = raw[:,:,:]

    if args.flipX == True:
    	flipx(raw, flip_raw)
        tmp[:,:,:] = flip_raw[:,:,:]

    if args.flipZ == True:
    	flipz(tmp, flip_raw)


