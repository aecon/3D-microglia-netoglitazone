# 3D-microglia-netoglitazone

**Under Development. The corresponding publication will be available soon.**

Image processing tools for the segmentation of microglia cells in 3D mouse brain data.


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


## Input Data

Tif stacks (3D image data) of mouse brain hemispheres, obtained with light-sheet microscopy (mesoSPIM), imaged across the sagittal plane.


## Contents
The directories `pre-processing`, `processing` and `plotting` contain tools to detect microglia cells from 3D mouse hemispheres, perform statistical analysis and generate figures for the corresponding publication.

### pre-processing:
Tools for stack pre-processing:
* Conversion of image stacks from tif to raw/nrrd file formats
* Cropping of image stacks to exclude large empty regions
* Flipping of stacks (horizontal and/or stack flip) to match the Allen Brain Atlas orientation.

### processing:
Main pipeline for image processing of 3D stacks.
* Cell segmentation: Detection of candidate microglia cells in 3D.
* Alignment: Hemisphere registration to Allen Brain Atlas Reference space.
* Removal of surface artefacts: To remove surface artifacts and perform voxelization of aligned cells.
* Voxelization**: Gaussian smoothing, with diameter 15 pixels

### plotting:
Tools to perform statistical analysis and generate paper figures.


## Authors
The pipeline was developed in the laboratories of Prof. Petros Koumoutsakos (Harvard University) and Prof. Adriano Aguzzi (University of Zurich) by
* [Athena Economides](https://athenaeconomides.com)
* Francesca Catto
* Sergey Litvinov


## Remaining TODOs
* Add python packages inside requirements.txt


