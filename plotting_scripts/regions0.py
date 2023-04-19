import adv
import collections
import mmap
import numpy
import sys
import skimage.io

me = "regions0.py"
def usg():
    sys.stderr.write("%s -i file.vtk -o file.vtk -a atlas.nrrd [-c]\n" % me)
    sys.exit(2)

input_path = None
output_path = None
atlas_path = "/media/athena-admin/FastSSD1/Athena/atlas/ABA_25um_annotation.tif" #"/media/athena-admin/FastSSD1/Athena/0_SRC/ann.nrrd"
Select = (512, 315, 1089, 1065, 1097, 549) # all regions
while True:
    sys.argv.pop(0)
    if len(sys.argv) and len(sys.argv[0]) > 1 and sys.argv[0][0] == '-':
        if sys.argv[0][1] == 'h':
            usg()
        elif sys.argv[0][1] == 'c':
            Select = (315,) # isocortex
        elif sys.argv[0][1] == 'i':
            try:
                sys.argv.pop(0)
                input_path = sys.argv[0]
            except IndexError:
                sys.stderr.write("%s: not enough arguments for -i\n" % me)
        elif sys.argv[0][1] == 'o':
            try:
                sys.argv.pop(0)
                output_path = sys.argv[0]
            except IndexError:
                sys.stderr.write("%s: not enough arguments for -o\n" % me)
                sys.exit(2)
        elif sys.argv[0][1] == 'a':
            try:
                sys.argv.pop(0)
                atlas_path = sys.argv[0]
            except IndexError:
                sys.stderr.write("%s: not enough arguments for -o\n" % me)
                sys.exit(2)
        else:
            sys.stderr.write("%s: unknown option '%s'\n" % (me, sys.argv[0]))
            sys.exit(2)
    else:
        break
if input_path == None:
    sys.stderr.write("%s: -i is not set\n" % me)
    sys.exit(2)
if output_path == None:
    sys.stderr.write("%s: -o is not set\n" % me)
    sys.exit(2)

atlas = skimage.io.imread(atlas_path, plugin='tifffile').T
alpha = 0.7
D = { }
Parent = { }
Acronym = { }
for id, parent, acronym, name, color in adv.atlas_data():
    red, green, blue = color
    D[id] = red, green, blue, alpha
    Parent[id] = parent
    Acronym[id] = acronym
D[0] = (0, 0, 0, 0)
for i in D:
    j = i
    while True:
        if j in Select:
            D[i] = D[j]
            Acronym[i] = Acronym[j]
            break
        if j == -1:
            D[i] = (0.99, 0.99, 0.99, alpha)
            Acronym[i] = "Other"
            break
        j = Parent[j]
cells = adv.points_read(input_path)
point = [ ]
color = [ ]
Counter = collections.Counter()
for x, y, z in cells:
    key = atlas[x, y, z]
    point.append((x, y, z))
    color.append((D[key]))
    Counter[Acronym[key]] += 1
dtype = numpy.dtype(">f4")
n = len(point)
with open(output_path, "wb") as f:
    f.write(b"""\
# vtk DataFile Version 2.0
adv.py
BINARY
DATASET POLYDATA
POINTS %d float
""" % n)
    points_offset = f.tell()
    f.seek(3 * n * dtype.itemsize - 1, 1)
    f.write(b'\0')
    f.write(b"""\
POINT_DATA %d
SCALARS color float 4
LOOKUP_TABLE default
""" % n)
    color_offset = f.tell()
    f.seek(4 * n * dtype.itemsize - 1, 1)
    f.write(b'\0')
with open(output_path, "r+") as f:
    buffer = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_WRITE)
    point0 = numpy.ndarray((n, 3), dtype, buffer, points_offset)
    buffer = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_WRITE)
    color0 = numpy.ndarray((n, 4), dtype, buffer, color_offset)

numpy.copyto(color0, color)
numpy.copyto(point0, point)
for k in Counter:
    print(k, Counter[k])
