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

The location of the data should be stored in the environment variable `${DATA}`.



## Image Processing

### pre-processing

* **Data Cropping**: used to crop out large empty regions.
```
cd pre-processing
./run_crop.sh
```

* **Data Flipping**: used to flip samples such that cerebellum is always on the LEFT.
```
cd pre-processing
python3 flip.py -i <path to nrrd file>
```


### main pipeline

* **Cell segmentation**: Edit parameters inside `./run_cell_detection_WREN.sh`. Then run as follows: 
```
./run_cell_detection_WREN.sh
```

* **Alignment to Allen Brain Atlas**: Uses [ClearMap](https://github.com/ChristophKirst/ClearMap2) and parameter files from `align/`
```
./run_align.sh
```

* **Removal of surface artefacts**: To remove surface artifacts and perform voxelization of aligned cells:
```
./run_erode.sh
```

* **Voxelization**: Gaussian smoothing, with diameter 15 pixels
```
run_voxelize.sh
```

### post-processing
Plotting and data analysis scripts are located inside folder `post-processing`. To generate all figures:
```
cd post-processing
./plot_all_figures.sh
```


## Authors
The pipeline was developed in the laboratories of Prof. Petros Koumoutsakos (Harvard University) and Prof. Adriano Aguzzi (University of Zurich) by
* Athena Economides
* Francesca Catto
* Sergey Litvinov
