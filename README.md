# 3D-microglia-netoglitazone

**Under Development. The corresponding publication will be available soon.**

Image processing pipeline for the segmentation of microglia cells in 3D mouse brain data.



## Requirements

* [img3D](https://github.com/aecon/img3D)
* [elastix](https://elastix.lumc.nl)
* [Fiji](https://fiji.sc)
* [AllenSDK](https://allensdk.readthedocs.io/en/latest)
* Python packages (see below)


### Python package installation

Create a new conda environment.
```
conda create -n "netoglitazone3D" python=3.7
```

Activate the environment.
```
conda activate netoglitazone3D
```

Install python packages.
```
pip install -r requirements.txt
```

<!---
I installed like this:
    conda install TODO:XXXX
-->



## Data

Tif stacks (3D image data) of mouse brain hemispheres, obtained with light-sheet microscopy (mesoSPIM), imaged across the sagittal plane.



## Image Processing

### pre-processing
* **Conversion of tif to raw/nrrd**: Required to use all other scripts.

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
