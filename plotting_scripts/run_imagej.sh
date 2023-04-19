#!/bin/bash
set -eu

GROUP=$1
neg=$2
pos=$3

# atlas
atlas=`dirname $2`/atlas_rot.nrrd

# outfile: Overlay of Atlas and Pos and Neg
out=`dirname ${neg}`"/pv_cells_group${GROUP}_Merge_corrected.tif"

/home/athena-admin/Desktop/Fiji.app/ImageJ-linux64 --headless -macro Macro.ijm "${atlas}","${pos}","${neg}","${out}"
