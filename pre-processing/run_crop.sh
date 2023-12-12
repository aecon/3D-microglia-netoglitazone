#!/bin/bash
set -eu


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# User settings
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# * DATA: Path to the directory containing
#   the data (see variable DATA below).
#
# * Input data:
#   - Must be in raw/nrrd format. To create 
#     raw/nrrd files from the tif files, see
#     the script: pre-processing/tif_to_raw.py
#   - Filenames: raw_SAMPLE.tif.nrrd, where SAMPLE
#     is the sample ID (e.g. first column in file 
#     corners.dat

DATA="3D-microglia-netoglitazone/data"



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Processing
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

while read l; do
    
    sample=`echo $l | awk '{print $1}'`
    if [ "$sample" != "sample" ]; then
        x0=`echo $l     | awk '{print $2}'`
        y0=`echo $l     | awk '{print $3}'`
        x1=`echo $l     | awk '{print $4}'`
        y1=`echo $l     | awk '{print $5}'`
    
        echo "$l"

        input="${DATA}/raw_${sample}.tif.nrrd"

        if [ -f "${input}" ]; then
            ls "Cropping:" $input
            python3.8 crop.py -i "${input}" -x0 $x0 -y0 $y0 -x1 $x1 -y1 $y1
        else
            echo "NOT FOUND: ${input}"
        fi

    fi
done <corners.dat

