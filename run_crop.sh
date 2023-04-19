#!/bin/bash
set -eu

d="/media/athena-admin/FastSSD1/Athena/francesca_202203/data"

while read l; do
    
    sample=`echo $l | awk '{print $1}'`
    if [ "$sample" != "sample" ]; then
        x0=`echo $l     | awk '{print $2}'`
        y0=`echo $l     | awk '{print $3}'`
        x1=`echo $l     | awk '{print $4}'`
        y1=`echo $l     | awk '{print $5}'`
    
        echo "$l"

        input="${d}/raw_${sample}.tif.nrrd"

        if [ -f "${input}" ]; then
            ls $input
            python3.8 crop_raw.py -i "${input}" -x0 $x0 -y0 $y0 -x1 $x1 -y1 $y1
        else
            echo "NOT FOUND: ${input}"
        fi

    fi
done <corners.dat

