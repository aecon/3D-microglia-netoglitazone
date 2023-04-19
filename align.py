import adv
import argparse
import array
import ClearMap.Alignment.Annotation as ano
import ClearMap.Alignment.Elastix as elx
import ClearMap.Alignment.Resampling as res
import ClearMap.Analysis.Measurements.Voxelization as vox
import ClearMap.IO.IO as io
import numpy as np
import os
import skimage.io
import sys
import tempfile
import tifffile

me = "align.py"

def flush(a):
    if hasattr(a.base, "flush"):
        if verbose:
            sys.stderr.write("%s: flush\n" % me)
        a.base.flush()


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

def nrrd_details(fnrrd):
    nrrd        = adv.nrrd_read(fnrrd)
    dtype       = nrrd["type"]
    path        = nrrd["path"]
    shape       = nrrd["sizes"]
    offset      = nrrd.get("byte skip", 0)
    dx, dy, dz  = nrrd.get("spacings")
    return dtype, path, shape, offset, dx, dy, dz

parser = argparse.ArgumentParser()
parser.add_argument('-i', type=str, required=True, help="input data (nrrd of original raw file)")
parser.add_argument('-o', type=str, required=True, help="output directory")
parser.add_argument('-k', type=int, required=True, nargs='+', help="stride (int int int)")
parser.add_argument('-d', type=float, required=True, nargs='+', help="spacing (float float float)")
parser.add_argument('-truecells', type=str, required=True, help="cells.nrrd")
parser.add_argument('-Iavg_min', type=float, default=0, help="minimum allowed average intensity from main.raw")

parser.add_argument('-azmin', type=int, required=True, help="index of first atlas slice in z")
parser.add_argument('-azmax', type=int, required=True, help="index of last atlas slice in z")
parser.add_argument('-ori', type=int, nargs='+', help="order and orientation of axis 1,2,3 (int int int)")
parser.add_argument('-affine', type=str, required=True, help="path to affine_parameter_file")
parser.add_argument('-bspline', type=str, required=True, help="path to bspline_parameter_file")

parser.add_argument('-N', type=int, default=None, help="number of processes")
parser.add_argument('-v', action='store_true', help='verbose')
args = parser.parse_args()


# tmp dir
mytmp = os.path.join(args.o, 'tmp')
if not os.path.exists(mytmp):
    os.makedirs(mytmp, exist_ok=True)
os.environ["TMPDIR"]=mytmp


# number of processes
if args.v:
    print("Running with %d processes." % args.N)
os.environ["OMP_NUM_THREADS"] = str(args.N)


# data parameters
verbose=args.v
if len(args.ori) != 3:
    sys.stderr.write("%s: -ori needs three arguments\n" % me)
    sys.exit(1)
ox, oy, oz = args.ori
if len(args.k) != 3:
    sys.stderr.write("%s: -k needs three arguments\n" % me)
    sys.exit(1)
kx, ky, kz = args.k
if len(args.d) != 3:
    sys.stderr.write("%s: -d needs three arguments\n" % me)
    sys.exit(1)
dx, dy, dz = args.d
if not os.path.exists(args.o):
    os.makedirs(args.o)
atlas_dir = "%s/%s" % (args.o, 'atlas')
if not os.path.exists(atlas_dir):
    os.makedirs(atlas_dir)

try:
    img_stack = adv.nrrd_data(args.i)
except FileNotFoundError:
    sys.stderr.write("%s: file not found '%s'\n" % (me, args.i))
    sys.exit(1)
except ValueError:
    sys.stderr.write("%s: wrong size/type '%s'\n" % (me, args.i))
    sys.exit(1)
img_stack = img_stack[::kx,::ky,::kz]
source_shape = img_stack.shape
nx, ny, nz = source_shape
dx *= kx
dy *= ky
dz *= kz


# Crop atlas files to data range
#   annotation_file: cropped annotation file - looks like corrupt images
#   reference_file: cropped reference file - nice images from atlas mouse brain
#   distance_file: distance cropped file - heatmap style
#
#   original atlas: 456 z-levels. slice(0,256) uses slices 0-255 only!!
#   original atlas image resolution: 320x528 pixels
#   x-y slicing is cropping the image.
#
#   orientation=(1,2,3): directions x,y,z. Re-orients the atlas files
annotation_file, reference_file, distance_file=ano.prepare_annotation_files(
    slicing=(slice(None),slice(None),slice(args.azmin,args.azmax)), orientation=(ox,oy,oz),
    verbose=True, directory="%s/atlas" % args.o, postfix="sliced", overwrite=True)



working_stack = adv.mmap_create("%s/stitched.npy" % args.o, np.dtype("uint16"), img_stack.shape)
working_stack[:,:,:] = img_stack[:,:,:]
flush(working_stack)

if 1:
    # resampling to atlas resolution
    resample_parameter = {
        "source_resolution" : (dx, dy, dz),
        "sink_resolution"   : (25, 25, 25),
        "processes"         : 'serial',
        "method"            : "memmap",
        "verbose"           : verbose,
        }
    resampled = res.resample(source=working_stack.T, **resample_parameter) # this is a very small file ~200 MB
    tifffile.imsave("%s/%s.tif" % (args.o, "resampled"), resampled)  # nz, ny, nx
    print("working_stack", np.shape(working_stack)) # nx, ny, nz
    print("resampled", np.shape(resampled.T)) # nx, ny, nz

if 1:
    # alignment: atlas to data
    # to be able to transpose cell locations later to
    # atlas space, we have to align here: atlas -> data
    align_reference_parameter = {
        "moving_image" : reference_file,
        "fixed_image"  : "%s/resampled.tif" % args.o,
        "result_directory" :  os.path.join(args.o, 'elastix_atlas_to_data'),
        "affine_parameter_file"  : args.affine,
        "bspline_parameter_file" : args.bspline,
        "processes" : args.N
        }

    if verbose:
        print("RUNNING ELASTIX: Aligning ...")
    elx.align(**align_reference_parameter)


if 1:
    # alignment: data to atlas
    # to plot image in the space of atlas
    align_reference_parameter2 = {
        "moving_image" : "%s/resampled.tif" % args.o,
        "fixed_image"  : reference_file,
        "result_directory" :  os.path.join(args.o, 'elastix_data_to_atlas'),
        "affine_parameter_file"  : args.affine,
        "bspline_parameter_file" : args.bspline,
        "processes" : args.N
        }

    if verbose:
        print("RUNNING ELASTIX: Aligning ...")
    elx.align(**align_reference_parameter2)



# cell detection
# shape must be: (XXX, 3)
print("CELL DETECTION PART")
dtypeC, pathC, shapeC, offsetC, dxC, dyC, dzC = nrrd_details(args.truecells)
cell_counts = read_input(args.truecells, me, pathC, dtypeC, offsetC, shapeC)
coordinates = np.where( cell_counts == 1 )
coordinates = np.transpose(coordinates)
assert(working_stack.shape == cell_counts.shape)

# remapping cell coordinates to atlas resolution (25um^3)
resample_parameter_cells = {
    "source_shape" : working_stack.shape,
    "sink_shape"   : io.shape("%s/resampled.tif" % args.o),
    "sink"         : None,
    "orientation"  : None,
    }
coordinates_transformed = res.resample_points(source=coordinates, **resample_parameter_cells)
coordinates_transformed = coordinates_transformed.astype(int)
#print("CHECK: max(x), max(y), max(z)", np.max(coordinates_transformed[:,0]), np.max(coordinates_transformed[:,1]), np.max(coordinates_transformed[:,2]))

counts_transformed = np.zeros(io.shape("%s/resampled.tif" % args.o))
#print("CHECK: np.shape(counts_transformed):", np.shape(counts_transformed))
for r in coordinates_transformed:
    counts_transformed[r[0], r[1], r[2]] += 1
coordinates_transformed = np.where( counts_transformed>0 )
coordinates_transformed = np.transpose(coordinates_transformed)
#print(coordinates_transformed)

# cell alignment to atlas
coordinates_aligned= elx.transform_points(
                coordinates_transformed, sink=None,
                transform_directory="%s/elastix_atlas_to_data" % args.o,
                result_directory="%s/elastix_cells_to_atlas" % args.o,
                binary=False, indices=True)

print("Storing transformed cells")
coords_array_trans = adv.mmap_create("%s/transformed_cells.raw" % args.o, np.dtype("uint16"), (320,528,(args.azmax-args.azmin)))
adv.nrrd_write("%s/transformed_cells.nrrd" % args.o, "%s/transformed_cells.raw" % args.o, coords_array_trans.dtype, coords_array_trans.shape, (1, 1, 1))

coordinates_aligned = coordinates_aligned.astype(int)
coords_array_trans[:,:,:] = 0
adist = skimage.io.imread(distance_file,  plugin='tifffile')
points = [ ]
print("Processing coordinates_aligned:", np.shape(coordinates_aligned), np.shape(coordinates_transformed))
for i, r in enumerate(coordinates_aligned):
    rx = int(r[0])
    ry = int(r[1])
    rz = int(r[2])
    if rx>=0 and rx<320 and ry>=0 and ry<528 and rz>=0 and rz<(args.azmax-args.azmin):
        if adist[rz,ry,rx] != 0: # remove cells outside of atlas brain surface
            rx0 = rx if args.ori[0] == 1 else 320 - rx - 1
            lr = coordinates_transformed[i]
            ct = counts_transformed[ lr[0], lr[1], lr[2] ]
            assert(ct>0)
            for ic in range(int(ct)):
                points.append( (rx0, ry, rz ) )
            coords_array_trans[rx0, ry, rz] = ct
flush(coords_array_trans)
print("Writing cells.vtk")
adv.points_write("%s/cells.vtk" % args.o, points)


## voxelization
#print("Voxelization")
#voxelization_parameter = dict(
#      shape = io.shape(annotation_file),
#      dtype = None,
#      weights = None,
#      method = 'sphere',
#      radius = (3,3,3),
#      kernel = None,
#      processes = None,
#      verbose = True
#    )
#vox.voxelize(np.array(points), sink="%s/voxelized.tif" % args.o, **voxelization_parameter)
