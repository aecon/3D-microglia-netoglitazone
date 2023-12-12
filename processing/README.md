# processing

Tools to perform microglia cell detection from 3D mouse hemispheres, and registration to the [Allen Mouse Brain Reference Atlas](http://atlas.brain-map.org).


## 1. segmentation

```
python segmentation.py -i "PATH/TO/SIGNAL/DATA/NRRD" -o "PATH/TO/OUTPUT/DIRECTORY" -Imin IMIN -Imax IMAX -v -p
```
where `IMIN` and `IMAX` are intensity thresholds for the minimum and maximum normalized microglia intensity.


To automate the segmentation over all samples, adapt the paths and the intensity thresholds inside `run_segmentation` and run as:
```
./run_segmentation.sh
```


## 2. artifact exclustion

Exclusion of antibody accumulation artifacts from sample surface and ventricles.

Usage:
```
python artifact_exclusion.py -i "PATH/TO/SEGMENTED/CELLS/NRRD"
```

To automate the artifact exclusion over all samples, adapt the paths to the transformed segmented cells, inside `run_artifact_exclusion.sh`, and run as:
```
./run_artifact_exclusion.sh
```


## 3. registration

Local transformation of samples for spatial registration on the [Allen Mouse Brain Reference Atlas](http://atlas.brain-map.org) data. Registration is performed by the script `registration.py`, using [elastix](https://elastix.lumc.nl).  

To use the `registration.py` script, the following variables need to be set:
* `IMAGEJPATH` (inside `registration.py`): path to the ImageJ executable on your computer.
* `ELASTIX_PATH` (inside elastix/run_elastix.sh): path to the elastix installation.
* Your ImageJ Input/Output settings should be set to the default values (save tiff/raw in big endian format).

Usage:
```
python registration.py -o "PATH/TO/OUTPUT/DIRECTORY" -a "PATH/TO/AUTOFLUORESCENCE/NRRD" -s "PATH/TO/SEGMENTED/CELLS/NRRD"
```


## 4. voxelization

Apply a Gaussian blur on the transformed segmented cells to allow for visual inspection of detected cell density on low resolution figures.

Usage:
```
python voxelization.py -i "PATH/TO/TRANSFORMED/CELLS/NRRD"
```

To automate the voxelization over all samples, adapt the paths to the transformed segmented cells, inside `run_voxelize.sh`, and run as:
```
./run_voxelize.sh
```

