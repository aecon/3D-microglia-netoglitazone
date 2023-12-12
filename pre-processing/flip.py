import os
import sys
import numba
import argparse
import numpy as np
import img3

# Needed flipping ("right" brains):
#   454371_17_LD_7
#   840258_3_LD_6

@numba.njit(parallel=True)
def flipx(a, out):
    nx, ny, nz = a.shape
    for k in numba.prange(nz):
        for j in numba.prange(ny):
            for i in numba.prange(nx):
                out[i, j, k] = a[(nx-i-1), j, k]

parser = argparse.ArgumentParser()
parser.add_argument('-i', type=str, required=True, help="raw data, nrrd")
args = parser.parse_args()

raw = img3.nrrd_data(args.i)

odir    = os.path.dirname(args.i)
basename = os.path.basename(args.i)
flip_raw = img3.mmap_create("%s/flip_%s.raw" % (odir, basename), raw.dtype, raw.shape)
img3.nrrd_write("%s/flip_%s.nrrd" % (odir, basename), "%s/flip_%s.raw" % (odir, basename), flip_raw.dtype, flip_raw.shape, (1,1,1))

flipx(raw, flip_raw)

