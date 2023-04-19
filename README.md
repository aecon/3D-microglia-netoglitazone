# 3D-microglia-netoglitazone

Image processing pipeline for the segmentation of microglia cells in 3D mouse brain data.


## Requirements
* gcc
* OpenMP
* Python (packages: numpy pandas scipy numba scikit-image matplotlib)
* [img3D package](https://github.com/aecon/img3D)


## Data

3D image files obtained from Light-sheet microscopy.


## Image Processing

1. `run_copy_tif.sh`: Copy script to FastSSD and run from athena-admin user (to be able to access sa..._3)  
2. `run_tif2raw.sh  <PATH TO TIF FILES>`  
3. `run_crop.sh`  
4. [ `run_cell_detection_WREN.sh`: Check intensity threshold for Back.Eq. and Cell detection ]  
5. If needed: `flip.py` (see arguments) to make all brains LEFT. Replace cropped brains with flipped ones.!! 
6. `run_align.sh`  
7. `run_erode.sh`: To remove surface artifacts + Voxelize  
8. `run_voxelize.sh`: Gaussian smoothing, with (plaque) Diameter = 15 pixels  
8. `cd plotting_scripts; ./plot_all_figures.sh`

