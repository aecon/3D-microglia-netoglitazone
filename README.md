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

Tools for stack pre-processing:
* Conversion of image stacks from tif to raw/nrrd file formats
* Cropping of image stacks to exclude large empty regions
* Flipping of stacks (horizontal and/or stack flip) to match the Allen Brain Atlas orientation.


### processing

Main image processing steps.

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
* [Athena Economides](https://athenaeconomides.com)
* Francesca Catto
* Sergey Litvinov



## Remaining TODOs
* Add python packages inside requirements.txt


