import os
import sys
import argparse
import numpy as np
import img3
import skimage.io

parser = argparse.ArgumentParser()
parser.add_argument('-i', type=str, required=True, help="segmented cells, nrrd")
args = parser.parse_args()

# aligned cells
cells = img3.nrrd_data(args.i)

# atlas (shape: 320x528x456)
fatlasA="FastSSD/atlas/ABA_25um_annotation.tif"
fatlasD="FastSSD/atlas/ABA_25um_distance_to_surface.tif"
atlasA = skimage.io.imread(fatlasA, plugin='tifffile').T
atlasD = skimage.io.imread(fatlasD, plugin='tifffile').T
atlasA = atlasA[:,:,0:np.shape(cells)[2]]
atlasD = atlasD[:,:,0:np.shape(cells)[2]]

# arrays
odir    = os.path.dirname(args.i)
keep    = img3.mmap_create("%s/keep.raw" % odir, np.dtype("uint8"), cells.shape)
tmp     = img3.mmap_create("%s/tmp.raw" % odir, np.dtype("uint8"), cells.shape)
eroded  = img3.mmap_create("%s/transformed_cells_eroded.raw" % odir, cells.dtype, cells.shape)
img3.nrrd_write("%s/transformed_cells_eroded.nrrd" % odir, "%s/transformed_cells_eroded.raw" % odir, eroded.dtype, eroded.shape, (1,1,1))

# erode perimeter of atlas
tmp[:,:,:] = atlasD[:,:,:]
tmp[tmp>0] = 1
img3.erosion(tmp, 2, keep)

# remove stuff out of eroded atlas (perimetrically)
eroded[:,:,:] = cells[:,:,:]
eroded[keep==0] = 0

# make a hole in the atlas: ITEM 81
eroded[atlasA==81] = 0

# visualization
if 0:
    # Caution: Overwrites values in file "transformed_cells_eroded.raw"
    eroded[(eroded>0) * (cells>0)] = 2
    eroded[(eroded==0) * (cells>0)] = 1

# voxelization
if 1:
    print("Voxelization")
    import ClearMap.Analysis.Measurements.Voxelization as vox

    points0 = img3.points_read("%s/cells.vtk" % os.path.dirname(args.i))
    points = []

    for p in points0:
        if eroded[p[0], p[1], p[2]] > 0:
            points.append(p)

    print("Writing cells_eroded.vtk")
    img3.points_write("%s/cells_eroded.vtk" % os.path.dirname(args.i), points)

    voxelization_parameter = dict(
          shape = cells.shape,
          dtype = None,
          weights = None,
          method = 'sphere',
          radius = (3,3,3),
          kernel = None,
          processes = None,
          verbose = True
        )
    print(np.shape(points0))
    print(np.shape(points))
    vox.voxelize(np.array(points), sink="%s/voxelized.tif" % os.path.dirname(args.i), **voxelization_parameter)

