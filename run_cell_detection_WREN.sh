#!/bin/bash
set -eu

# ~~~~~~~~~~~ DATA ~~~~~~~~~~~ #
di=/media/athena-admin/FastSSD1/Athena/francesca_202203/data/cropped
#samples=("340258_2LD_5" "454371_17_LD_7" "840298_52_P_20" "340299_35_22_HD" "840258_3_LD_6" "840298_16_P_17" "840298_50_P_19" "840295_42_HD")  # Imin=150
samples=("840295_40_HD_27")  # Imin=130
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


for sample in ${samples[@]}; do

    input=`find ${di} -name "cropped_raw_${sample}*.nrrd"`
    ls $input

    outdir="/media/athena-admin/FastSSD1/Athena/francesca_202204/out_filter647_01/${sample}"
    mkdir -p "${outdir}"

    Imin=130 #150
    Imax=2000
    echo $sample $Imin $Imax

    python3.8 cell_detection_WREN.py -i "${input}" -o "${outdir}" -Imin $Imin -Imax $Imax -v -p


    # remove helper files
    rm "${outdir}"/segment/mask.raw
    rm "${outdir}"/segment/mask_erosion.raw
    rm "${outdir}"/segment/tmp8.raw
    rm "${outdir}"/segment/tmp32a.raw
    rm "${outdir}"/segment/tmp32b.raw
    rm "${outdir}"/segment/labels.raw
    rm "${outdir}"/segment/work.raw
    rm "${outdir}"/segment/denoised.raw

done

