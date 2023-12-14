#!/bin/bash
set -eu


base0="/FastSSD1/Athena/francesca_202203/out_filter647_01"  #location: ${sample}/align"

samples=("340258_2LD_5" "840298_52_P_20" "340299_35_22_HD" "840298_16_P_17" "840298_50_P_19" "840295_42_HD" "840295_40_HD_27" "840258_3_LD_6" "454371_17_LD_7")


# Gaussian smoothing ``radius''
# 3 for segmentation visualiation. 15 for pvalues (same as plaque post-processing).
R=15
if [ ${R} -eq "0" ]; then
    tifname="voxelized.tif"
else
    tifname="voxelized_R${R}.tif"
fi
echo "Using file: $tifname"

# Make figures directory
ofig=$base0/figures_R${R}
mkdir -p $ofig


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Coronal slices of density per sample
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if false; then
    for sample in ${samples[@]}; do
   
        base="${base0}/${sample}/align"

        lv=${base}/${tifname}
        if [ -f "${lv}" ]; then
            ls -d "${base}"
            ls $lv
            python3.6 coronal_per_sample.py -i $lv -o ${ofig} -s $sample
        else
            echo "File ${lv} not found!"
            exit
        fi
    done
fi


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Sample Groups
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# 01_P: CONTROL
samples1=("840298_52_P_20" "840298_16_P_17" "840298_50_P_19")
# 02_LD: LOW DOSE
samples2=("340258_2LD_5" "840258_3_LD_6" "454371_17_LD_7")
# 03_HD: HIGH DOSE
samples3=("340299_35_22_HD" "840295_42_HD" "840295_40_HD_27")

 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Average distribution per group
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if false; then
    files=""
    counter=0
    for s in ${samples1[@]}; do
        files="$files $base0/${s}/align/${tifname}"
        counter=`awk -v c=$counter 'BEGIN {print c+1}'`
    done
    odir=${base0}/processed_R${R}
    mkdir -p $odir
    python3.8 plot_avg_density.py -i $files -on "blur" -o $odir -g 1 -of ${ofig}

    files=""
    counter=0
    for s in ${samples2[@]}; do
        files="$files $base0/${s}/align/${tifname}"
        counter=`awk -v c=$counter 'BEGIN {print c+1}'`
    done
    odir=${base0}/processed_R${R}
    mkdir -p $odir
    python3.8 plot_avg_density.py -i $files -on "blur" -o $odir -g 2 -of ${ofig}
    
    files=""
    counter=0
    for s in ${samples3[@]}; do
        files="$files $base0/${s}/align/${tifname}"
        counter=`awk -v c=$counter 'BEGIN {print c+1}'`
    done
    odir=${base0}/processed_R${R}
    mkdir -p $odir
    python3.8 plot_avg_density.py -i $files -on "blur" -o $odir -g 3 -of ${ofig}

    if false; then
        # MONTAGE
        files=`ls ${ofig}/pic_density_coronal_AVG_*png`
        counter=3
        echo $files
        montage $files -geometry +0+0 -tile 1x"${counter}" ${ofig}/pic_density_coronal_AVG_montage_blur.png
    fi

fi


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# pvalue between saline and groups 1/2
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if false; then
    R=15
    python3.8 plot_pvalue_overlay_to_saline.py   -f1  ${base0}/processed_R${R}/avg_cells_group2.nrrd -f2  ${base0}/processed_R${R}/avg_cells_group1.nrrd \
                                                 -f1s ${base0}/processed_R${R}/std_cells_group2.nrrd -f2s ${base0}/processed_R${R}/std_cells_group1.nrrd \
                                                 -g 2 -o ${ofig} -R $R

    python3.8 plot_pvalue_overlay_to_saline.py   -f1  ${base0}/processed_R${R}/avg_cells_group3.nrrd -f2  ${base0}/processed_R${R}/avg_cells_group1.nrrd \
                                                 -f1s ${base0}/processed_R${R}/std_cells_group3.nrrd -f2s ${base0}/processed_R${R}/std_cells_group1.nrrd \
                                                 -g 3 -o ${ofig} -R $R
fi


if true; then
    R=15
    echo "Running Cluster Correction"
    python3.8 cluster_correct.py -p ${base0}/processed_R${R}/pv_cells_group2_pos.nrrd
    python3.8 cluster_correct.py -p ${base0}/processed_R${R}/pv_cells_group2_neg.nrrd
    python3.8 cluster_correct.py -p ${base0}/processed_R${R}/pv_cells_group3_pos.nrrd
    python3.8 cluster_correct.py -p ${base0}/processed_R${R}/pv_cells_group3_neg.nrrd

    exit
    echo "Merge channels"
    GROUP=2; ./run_imagej.sh ${GROUP} ${base0}/processed_R${R}/pv_cells_group${GROUP}_neg_corrected.nrrd ${base0}/processed_R${R}/pv_cells_group${GROUP}_pos_corrected.nrrd
    GROUP=3; ./run_imagej.sh ${GROUP} ${base0}/processed_R${R}/pv_cells_group${GROUP}_neg_corrected.nrrd ${base0}/processed_R${R}/pv_cells_group${GROUP}_pos_corrected.nrrd

fi

exit


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Statistics per region
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if false; then
    # run as: ./runall_regions.sh <list of cells_eroded.vtk files>
    files=`ls ${base0}/*/align/cells_eroded.vtk`
    for f in ${files[@]}; do
        echo $f
    
        # output all regions
        cm.python regions0.py -i $f -o ${f}.vtk > ${f}.out

    done
    
    ./run_regions_collect.sh ${base0}/*/align/cells_eroded.vtk.out > data_regions.dat
fi

# Plot region statistics
if true; then
    python3.8 plot_regions.py -o ${ofig}
fi
