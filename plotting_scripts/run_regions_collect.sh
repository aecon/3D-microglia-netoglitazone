#!/bin/bash
# run as: ./me.sh <list of merged_cells.vtk.out files>

set -eu

# Sorted:
# 1 CB 819496
# 2 HB 452692
# 3 HPF 682678
# 4 HY 117093
# 5 Isocortex 2005659
# 6 Other 2928295
# 7 TH 51202

printf "%10s %10s %10s %10s %10s %10s %10s\n" "Sample" "CB" "HB" "HPF" "HY" "IC" "TH"
for f; do

    id=`echo $f | awk -F  "out_filter647_01/" ' {print $2}' | awk -F  "/" ' {print $1}'`

    CB=`cat $f  | sort -g -k 1 | awk 'NR==1 {print $2}'`
    HB=`cat $f  | sort -g -k 1 | awk 'NR==2 {print $2}'`
    HPF=`cat $f | sort -g -k 1 | awk 'NR==3 {print $2}'`
    HY=`cat $f  | sort -g -k 1 | awk 'NR==4 {print $2}'`
    IC=`cat $f  | sort -g -k 1 | awk 'NR==5 {print $2}'`
    TH=`cat $f  | sort -g -k 1 | awk 'NR==7 {print $2}'`

    printf "%15s %10d %10d %10d %10d %10d %10d\n" $id $CB $HB $HPF $HY $IC $TH
done
