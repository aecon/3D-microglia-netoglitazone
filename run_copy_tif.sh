#!/bin/bash
set -eu

o=/media/athena-admin/FastSSD1/Athena/francesca_202203/data


# filter 647 (microglia)
if false; then
    echo "CHANNEL 647"
    cp '/media/athena-admin/FastSSD1/Athena/annamaria/ilastik/sa3400_3/Francesca/Wren_Iba1-DISCO/340299_35_22_HD/R_STITCH_340299_35_22_HD/filter_647SG/rot_0/RES(5204x3670x1611)/000000/000000_0-1810/000000_0-1810_000570.tif' ${o}/raw_340299_35_22_HD.tif
    cp '/media/athena-admin/FastSSD1/Athena/annamaria/ilastik/sa3400_3/Francesca/Wren_Iba1-DISCO/840258_3_LD_#6/R_STITCH_840258_3_LD_#6/filter_647SG/rot_0/RES(5269x3670x1977)/000000/000000_0-1840/000000_0-1840_000600.tif' ${o}/raw_840258_3_LD_#6.tif
    cp '/media/athena-admin/FastSSD1/Athena/annamaria/ilastik/sa3400_3/Francesca/Wren_Iba1-DISCO/840295_40_HD_#27/R_STITCH_840295_40_HD_#27/filter_647SG/rot_0/RES(5202x3669x1514)/000000/000000_0-1870/000000_0-1870_000480.tif' ${o}/raw_840295_40_HD_#27.tif
    cp '/media/athena-admin/FastSSD1/Athena/annamaria/ilastik/sa3400_3/Francesca/Wren_Iba1-DISCO/840295_42_HD/R_STITCH_840295_42_HD/filter_647SG/rot_0/RES(5337x3643x1647)/000000/000000_0-1100/000000_0-1100_000570.tif' ${o}/raw_840295_42_HD.tif
    cp '/media/athena-admin/FastSSD1/Athena/annamaria/ilastik/sa3400_3/Francesca/Wren_Iba1-DISCO/840298_16_P_#17/R_STITCH_840298_16_P_#17/filter_647SG/rot_0/RES(5202x3667x1813)/000000/000000_0-1740/000000_0-1740_000570.tif' ${o}/raw_840298_16_P_#17.tif
    cp '/media/athena-admin/FastSSD1/Athena/annamaria/ilastik/sa3400_3/Francesca/Wren_Iba1-DISCO/840298_50_P_#19/R_STITCH_840298_50_P_#19/filter_647SG/rot_0/RES(5362x3669x1813)/000000/000000_0-1870/000000_0-1870_000510.tif' ${o}/raw_840298_50_P_#19.tif
    cp '/media/athena-admin/FastSSD1/Athena/annamaria/ilastik/sa3400_3/Francesca/Wren_Iba1-DISCO/840298_52_P_20/R_STITCH_840298_52_P_20/filter_647SG/rot_0/RES(5200x3666x1645)/000000/000000_0-1740/000000_0-1740_000630.tif' ${o}/raw_840298_52_P_20.tif
fi


# filter 520 (plaque)
if true; then
    echo "CHANNEL 520"
#    cp '/media/athena-admin/FastSSD1/Athena/annamaria/ilastik/sa3400_3/Francesca/Wren_Iba1-DISCO/840298_52_P_20/R_STITCH_840298_52_P_20/filter_520SG/rot_0/RES(5200x3666x1645)/000000/000000_0-1740/000000_0-1740_000630.tif' ${o}/raw_840298_52_P_20.tif
#    cp '/media/athena-admin/FastSSD1/Athena/annamaria/ilastik/sa3400_3/Francesca/Wren_Iba1-DISCO/340299_35_22_HD/R_STITCH_340299_35_22_HD/filter_520SG/rot_0/RES(5204x3670x1611)/000000/000000_0-1810/000000_0-1810_000570.tif' "${o}/raw_340299_35_22_HD.tif"
#    cp '/media/athena-admin/FastSSD1/Athena/annamaria/ilastik/sa3400_3/Francesca/Wren_Iba1-DISCO/840258_3_LD_#6/R_STITCH_840258_3_LD_#6/filter_520SG/rot_0/RES(5269x3670x1977)/000000/000000_0-1840/000000_0-1840_000600.tif' "${o}/raw_840258_3_LD_6.tif"
#    cp '/media/athena-admin/FastSSD1/Athena/annamaria/ilastik/sa3400_3/Francesca/Wren_Iba1-DISCO/840295_40_HD_#27/R_STITCH_840295_40_HD_#27/filter_520SG/rot_0/RES(5202x3669x1514)/000000/000000_0-1870/000000_0-1870_000480.tif' "${o}/raw_840295_40_HD_27.tif"
#    cp '/media/athena-admin/FastSSD1/Athena/annamaria/ilastik/sa3400_3/Francesca/Wren_Iba1-DISCO/840295_42_HD/R_STITCH_840295_42_HD/filter_520SG/rot_0/RES(5337x3643x1647)/000000/000000_0-1100/000000_0-1100_000570.tif' "${o}/raw_840295_42_HD.tif"
#    cp '/media/athena-admin/FastSSD1/Athena/annamaria/ilastik/sa3400_3/Francesca/Wren_Iba1-DISCO/840298_16_P_#17/R_STITCH_840298_16_P_#17/filter_520SG/rot_0/RES(5202x3667x1813)/000000/000000_0-1740/000000_0-1740_000570.tif' "${o}/raw_840298_16_P_17.tif"
#    cp '/media/athena-admin/FastSSD1/Athena/annamaria/ilastik/sa3400_3/Francesca/Wren_Iba1-DISCO/840298_50_P_#19/R_STITCH_840298_50_P_#19/filter_520SG/rot_0/RES(5362x3669x1813)/000000/000000_0-1870/000000_0-1870_000510.tif' "${o}/raw_840298_50_P_19.tif"

#    cp '/media/athena-admin/FastSSD1/Athena/annamaria/ilastik/sa3400_3/Francesca/Wren_Iba1-DISCO/454371_17_LD_#7/R_STITCH_454371_17_LD_#7/filter_520SG/rot_0/RES(5204x3670x1810)/000000/000000_0-1840/000000_0-1840_000540.tif' "${o}/raw_454371_17_LD_7.tif"
#    cp '/media/athena-admin/FastSSD1/Athena/annamaria/ilastik/sa3400_3/Francesca/Wren_Iba1-DISCO/340258#2LD#5/R_STITCH_340258#2LD#5/filter_520SG/rot_0/RES(5219x3668x2142)/000000/000000_0-1770/000000_0-1770_000090.tif' "${o}/raw_raw_340258_2LD_5.tif"

fi


