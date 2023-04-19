import os
import sys
import mmap
import numba
import argparse
import numpy as np
import adv

me = "crop_raw.py"


def nrrd_details(fnrrd):
    nrrd        = adv.nrrd_read(fnrrd)
    dtype       = nrrd["type"]
    path        = nrrd["path"]
    shape       = nrrd["sizes"]
    offset      = nrrd.get("byte skip", 0)
    dx, dy, dz  = nrrd.get("spacings")
    return dtype, path, shape, offset, dx, dy, dz

def read_input(argsi, me, path, dtype, offset, shape):
    try:
        a0 = np.memmap(path, dtype, 'r', offset=offset, shape=shape, order='F')
    except FileNotFoundError:
        sys.stderr.write("%s: file not found '%s'\n" % (me, argsi))
        sys.exit(1)
    except ValueError:
        sys.stderr.write("%s: wrong size/type '%s'\n" % (me, argsi))
        sys.exit(1)
    return a0


@numba.njit(parallel=True)
def crop(a, out, x0, y0):
    nx, ny, nz = out.shape
    for k in numba.prange(nz):
        for j in numba.prange(ny):
            for i in numba.prange(nx):
                out[i, j, k] = a[x0+i, y0+j, k]


parser = argparse.ArgumentParser()
parser.add_argument('-i', type=str, required=True, help="raw data, nrrd")
parser.add_argument('-x0', type=int, required=True)
parser.add_argument('-y0', type=int, required=True)
parser.add_argument('-x1', type=int, required=True)
parser.add_argument('-y1', type=int, required=True)
args = parser.parse_args()


# raw file
dtype, path, shape, offset, dx, dy, dz = nrrd_details(args.i)
img_stack = read_input(args.i, me, path, dtype, offset, shape)

shape = img_stack.shape
spacings = (dx, dy, dz)


# cropped file
Lx = args.x1 - args.x0
Ly = args.y1 - args.y0

foutr = "%s/cropped_%s.raw" % ( os.path.dirname(args.i), os.path.basename(args.i) )
foutn = "%s/cropped_%s.nrrd" % ( os.path.dirname(args.i), os.path.basename(args.i) )
cropped = adv.mmap_create(foutr, img_stack.dtype, [Lx,Ly,shape[2]])
adv.nrrd_write(foutn, foutr, cropped.dtype, cropped.shape, spacings)


# crop
crop(img_stack, cropped, args.x0, args.y0)


