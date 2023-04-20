#!/bin/bash
set -e

di=/media/athena-admin/FastSSD1/Athena/francesca_202203/data
do=/media/athena-admin/FastSSD1/Athena/francesca_202203/out_filter647_01
samples=("340258_2LD_5" "840298_52_P_20" "340299_35_22_HD" "840298_16_P_17" "840298_50_P_19" "840295_42_HD" "840295_40_HD_27" "454371_17_LD_7" "840258_3_LD_6")
#samples=("454371_17_LD_7")
#samples=("840298_52_P_20")

for s in ${samples[@]}; do

    echo $s

    python3.8 overlay_raw_segmented.py -r "${di}/cropped_647/cropped_raw_${s}.tif.nrrd.nrrd" -s "${do}/${s}/segment/segmented.nrrd" -id "${s}"

done
