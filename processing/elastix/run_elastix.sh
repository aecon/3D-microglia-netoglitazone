#!/bin/bash
set -eu

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# User settings
#
# - Set the path to the elastix folder
#   in the variable ELASTIX_PATH below.
# - Set the number of threads.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Path to elastix folder
ELASTIX_PATH=${HOME}/Downloads/elastix

# Number of threads
threads=32


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Processing
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if [ "$#" -ne 3 ]; then
    echo ">> Error:"
    echo ">> run_elastix.sh requires 3 input arguments."
    echo ">> run as: ./run_elastix.sh 'PATH/TO/OUTPUT/DIRECTORY' 'PATH/TO/AUTOFLUORESCENCE/CHANNEL' 'PATH/TO/SIGNAL/CHANNEL'"
    exit
fi

export LD_LIBRARY_PATH=${ELASTIX_PATH}/lib/
elastix="${ELASTIX_PATH}/bin/elastix"
transformix="${ELASTIX_PATH}/bin/transformix"

SCRIPT=$(realpath "$0")
SCRIPTPATH=$(dirname "$SCRIPT")

out=$1
input_auto=$2
input_seg=$3
echo $out
echo $input_auto
echo $input_seg


atlas=${SCRIPTPATH}/"atlas.nrrd"
affine=${SCRIPTPATH}/"affine.txt"
bspline=${SCRIPTPATH}/"bspline.txt"

outEa=${out}/elastix_affine
outEb=${out}/elastix_bspline
outT=${out}/transformix
mkdir -p ${outEa}
mkdir -p ${outEb}
mkdir -p ${outT}

# autofluorescence registration
${elastix} -out ${outEa} -f ${atlas} -m ${input_auto} -p ${affine} -threads $threads
${elastix} -out ${outEb} -f ${atlas} -m ${input_auto} -p ${bspline} -t0 ${outEa}/TransformParameters.0.txt  -threads $threads

# edit the Bspline file to use for transforming binary segmented data
cp ${outEb}/TransformParameters.0.txt ${outT}/
sed -i "/FinalBSplineInterpolationOrder/c\(FinalBSplineInterpolationOrder 0)" ${outT}/TransformParameters.0.txt

# apply transformation to segmentation
${transformix} -in ${input_seg} -out ${outT} -tp ${outT}/TransformParameters.0.txt -threads $threads



