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

### Location

The location of the data is assumed to be stored in the environment variable `${DATA}`.

Here `DATA=FastSSD1/Athena/francesca_202203/data`



## Image Processing

### pre-processing

* **Data Cropping**: used to crop out large empty regions.
```
cd pre-processing
./run_crop.sh
```

* **Data Flipping**: used to flip samples such that cerebellum is always on the Left.
```
cd pre-processing
python3 flip.py -i <path to nrrd file>
```


### main pipeline

* [ `run_cell_detection_WREN.sh`: Check intensity threshold for Back.Eq. and Cell detection ]  
* If needed: `flip.py` (see arguments) to make all brains LEFT. Replace cropped brains with flipped ones.!! 
* `run_align.sh`  
* `run_erode.sh`: To remove surface artifacts + Voxelize  
* `run_voxelize.sh`: Gaussian smoothing, with (plaque) Diameter = 15 pixels  
* `cd plotting_scripts; ./plot_all_figures.sh`


## Authors
The pipeline was developed in the laboratories of Prof. Petros Koumoutsakos (Harvard University) and Prof. Adriano Aguzzi (University of Zurich) by
* Athena Economides
* Francesca Catto
* Sergey Litvinov
