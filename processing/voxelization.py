import os
import sys
import argparse
import numpy as np
import img3
import ClearMap.Analysis.Measurements.Voxelization as vox

parser = argparse.ArgumentParser()
parser.add_argument('-i', type=str, required=True, help="segmented cells, nrrd")
args = parser.parse_args()

# aligned cells
cells = img3.nrrd_data(args.i)

points0 = img3.points_read("%s/cells_eroded.vtk" % os.path.dirname(args.i))
print(np.shape(points0))

points = np.zeros(np.shape(points0))
points[:,:] = points0[:,:]

print("Voxelization")
radius = 3  # 3 for visualizing segmented microglia, 15 for pvalue stats
voxelization_parameter = dict(
      shape = cells.shape,
      dtype = None,
      weights = None,
      method = 'sphere',
      radius = (radius,radius,radius),
      kernel = None,
      processes = None,
      verbose = True
    )
vox.voxelize(np.array(points), sink="%s/voxelized_R%d.tif" % (os.path.dirname(args.i), radius), **voxelization_parameter)

