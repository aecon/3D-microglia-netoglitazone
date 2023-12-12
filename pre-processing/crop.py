import os
import numba
import argparse
import numpy as np
import img3

me = "crop.py"

@numba.njit(parallel=True)
def crop_array(a, out, x0, y0):
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
dtype, path, shape, offset, dx, dy, dz = img3.nrrd_details(args.i)
img_stack = img3.read_input(args.i, me, path, dtype, offset, shape)

shape = img_stack.shape
spacings = (dx, dy, dz)

# cropped file
Lx = args.x1 - args.x0
Ly = args.y1 - args.y0

foutr = "%s/cropped_%s.raw" % ( os.path.dirname(args.i), os.path.basename(args.i) )
foutn = "%s/cropped_%s.nrrd" % ( os.path.dirname(args.i), os.path.basename(args.i) )
cropped = img3.mmap_create(foutr, img_stack.dtype, [Lx,Ly,shape[2]])
img3.nrrd_write(foutn, foutr, cropped.dtype, cropped.shape, spacings)

# crop
crop_array(img_stack, cropped, args.x0, args.y0)

