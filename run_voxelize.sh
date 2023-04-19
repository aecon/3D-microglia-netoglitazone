#!/bin/bash
set -eu


# ~~~~~~~~~~~ DATA ~~~~~~~~~~~ #
di=/media/athena-admin/FastSSD1/Athena/francesca_202203/data
samples=("340258_2LD_5" "840298_52_P_20" "340299_35_22_HD" "840298_16_P_17" "840298_50_P_19" "840295_42_HD" "840295_40_HD_27" "454371_17_LD_7" "840258_3_LD_6")
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


for sample in ${samples[@]}; do
    echo "SAMPLE: ${sample}"

    input="${di}/../out_filter647_01/${sample}/align/transformed_cells.nrrd"
    if [ -f "${input}" ]; then
        echo "INPUT:"; ls ${input}
        python3.6 voxelization.py -i "${input}"
    fi 

done
