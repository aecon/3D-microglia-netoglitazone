# 3D-microglia-netoglitazone

Image processing pipeline for the segmentation of microglia cells in 3D mouse brain data.


## Requirements

* C compiler
* numpy
* [img3D package](https://github.com/aecon/img3D)

### Optional requirements

* C compiler with OpenMP support
* ImageJ
* Python packages: tifffile, numba, scipy, scikit-image, pandas, matplotlib



## Data

3D image files obtained from Light-sheet microscopy.


## Image Processing

2. `run_tif2raw.sh  <PATH TO TIF FILES>`  
3. `run_crop.sh`  
4. [ `run_cell_detection_WREN.sh`: Check intensity threshold for Back.Eq. and Cell detection ]  
5. If needed: `flip.py` (see arguments) to make all brains LEFT. Replace cropped brains with flipped ones.!! 
6. `run_align.sh`  
7. `run_erode.sh`: To remove surface artifacts + Voxelize  
8. `run_voxelize.sh`: Gaussian smoothing, with (plaque) Diameter = 15 pixels  
8. `cd plotting_scripts; ./plot_all_figures.sh`


## Authors
The pipeline was developed in the laboratories of Prof. Petros Koumoutsakos (Harvard University) and Prof. Adriano Aguzzi (University of Zurich) by
* Athena Economides
* Francesca Catto
* Sergey Litvinov
