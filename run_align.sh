#!/bin/bash
set -eu


# ~~~~~~~~~~~ DATA ~~~~~~~~~~~ #
di=/media/athena-admin/FastSSD1/Athena/francesca_202203/data
samples=("340258_2LD_5" "840298_52_P_20" "340299_35_22_HD" "840298_16_P_17" "840298_50_P_19" "840295_42_HD" "840295_40_HD_27" "454371_17_LD_7" "840258_3_LD_6")
#samples=("454371_17_LD_7" "840258_3_LD_6") # right: -1
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


for sample in ${samples[@]}; do
    echo "SAMPLE: ${sample}"

    # USE PLAQUE CHANNEL FOR ALIGNMENT !!
    input=`find "${di}/cropped_520" -name "cropped_raw_${sample}*.nrrd"`
    echo "INPUT:"; ls ${input}
 
    truecells="${di}/../out_filter647_01/${sample}/segment/segmented.nrrd"
    echo "CELLS:"; ls ${truecells}

    outdir="${di}/../out_filter647_01/${sample}/align"
    mkdir -p "${outdir}"

    # side of Cerebellum: ALWAYS on the RIGHT: 1
    ox=1

    python3.6 align.py -i ${input} -o ${outdir} -k 1 1 1 -d 3.26 3.26 3.00 -azmin 0 -azmax 230 -ori $ox 2 3 -N 32 -truecells ${truecells} -affine data/affine.txt -bspline data/bspline.txt -v
    rm -rf ${outdir}/stitched.npy

done
