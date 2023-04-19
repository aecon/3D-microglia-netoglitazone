import os
import sys
import adv
import argparse
import matplotlib.pyplot as plt
import numpy as np
import skimage.io
from numpy.ma import masked_array
from matplotlib import cm
from matplotlib import colors
from matplotlib.colors import LinearSegmentedColormap


# group details
N = [3, 3, 3]

TITLES = ["Control","LD","HD"]

parser = argparse.ArgumentParser()
parser.add_argument('-i', type=str, required=True, nargs='+', help="input: voxelized.tif")
parser.add_argument('-on', type=str, required=True, help="outname")  # "real" or "blur"
parser.add_argument('-of', type=str, required=True, help="output folder for figure")  # "real" or "blur"
parser.add_argument('-o', type=str, required=True, help="outdir")
parser.add_argument('-g', type=int, required=True, help="group ID") # 1,2,3 corresponding to: Toxofilin-Cre or Gra16-Cre or saline
parser.add_argument('-a', type=str, default="/media/athena-admin/FastSSD1/Athena/atlas/ABA_25um_reference.tif", help="atlas file")
args = parser.parse_args()

samecolor=True

def coronal(ax, atlas, cells_masked, cmap, Vmax, Vmin, group, slices):
    print(args.on)
    for ic in range(Nc):
        i = slices[ic]
        pa = ax[ic].imshow(atlas[:,i,:], interpolation='nearest', cmap=cm.gray)

        alphas = ((cells_masked[:,i,:]))/Vmax; alphas[alphas<0.1]=0.1; alphas[alphas>1]=1
        pb = ax[ic].imshow(cells_masked[:,i,:], interpolation='nearest', cmap=cmap, alpha=alphas, vmin=Vmin, vmax=Vmax)

        ax[ic].set_axis_off()

        if ic==0:
            if args.g == 1:
                text="Control"
            elif args.g == 2:
                text="Low dose"
            elif args.g == 3:
                text = "High dose"
            ax[ic].annotate(text=text, xy=(16, 36), xycoords='data', color='w')

    plt.subplots_adjust(wspace=0, hspace=0)
    if samecolor == True:
        plt.savefig("%s/pic_density_coronal_AVG_allmagenta_g%d_%s_%s.pdf"%(args.of, group, TITLES[group-1], args.on), bbox_inches='tight', pad_inches=0, transparent=False)
    else:
        plt.savefig("%s/pic_density_coronal_AVG_g%d_%s_%s.pdf"%(args.of, group, TITLES[group-1], args.on), bbox_inches='tight', pad_inches=0, transparent=False)
    plt.close()



group = args.g; print(group)
vmin=0; vmax=4500 #3000
if samecolor == True:
    colors = [(1, 0, 1), (1, 0, 1)]
else:
    if group==1:
        colors = [(1, 0, 1), (1, 0, 1)]  # Magenta
    elif group==2:
        colors = [(0, 1, 1), (0, 1, 1)]  # Cyan
    elif group==3:
        colors = [(1, 1, 0), (1, 1, 0)]  # Yellow
    else:
        sys.exit()

cmap_name = 'my_list'
cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=100)



# load
atlas0 = skimage.io.imread(args.a, plugin='tifffile').T
tmpcells = skimage.io.imread(args.i[0], plugin='tifffile').T
atlas = np.zeros(np.shape(tmpcells))
atlas[:,:,:] = atlas0[:, :, 0:np.shape(tmpcells)[2]]
atlasshape = np.shape(atlas)


average = np.zeros(np.shape(atlas))
all_cells = []
for file in args.i:
    cells = skimage.io.imread(file, plugin='tifffile').T
    all_cells.append(cells)
average = np.mean(all_cells,axis=0)
staddev = np.std(all_cells,axis=0)

cells_masked = masked_array(average,average==0)



# write means
name_raw = "%s/avg_cells_group%d.raw"%(args.o, group)
name_nrrd = "%s/avg_cells_group%d.nrrd"%(args.o, group)
o = adv.mmap_create(name_raw, np.dtype("float"), atlasshape)
adv.nrrd_write(name_nrrd, name_raw, o.dtype, o.shape, (1,1,1))
o[:,:,:] = average[:,:,:]


# write stds
name_raw = "%s/std_cells_group%d.raw"%(args.o, group)
name_nrrd = "%s/std_cells_group%d.nrrd"%(args.o, group)
o2 = adv.mmap_create(name_raw, np.dtype("float"), atlasshape)
adv.nrrd_write(name_nrrd, name_raw, o2.dtype, o2.shape, (1,1,1))
o2[:,:,:] = staddev[:,:,:]


Nc=8
Nr=1
slices = [50, 100, 150, 200, 250, 300, 350, 400]
fig,ax = plt.subplots(Nr,Nc, figsize=(16,3), facecolor='black')
coronal(ax, atlas, cells_masked, cmap, vmax, vmin, group, slices)

