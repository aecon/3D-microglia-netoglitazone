#!/bin/bash
set -eu

L=/home/eceva/Documents/cells/poc

for f; do
    echo $f
    python3.8 ${L}/tif2raw.py -i "${f}" -o "${f}.raw" -n "${f}.nrrd" -v
    #rm -rf "${f}"
done
