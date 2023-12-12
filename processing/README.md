# processing

Tools to perform microglia cell detection from 3D mouse hemispheres.


## segmentation



## classification



## registration

Local transformation of samples for spatial registration on the [Allen Mouse Brain Reference Atlas](http://atlas.brain-map.org) data. Registration is performed by the script `registration.py`, using [elastix](https://elastix.lumc.nl).  

To use the `registration.py` script, the following variables need to be set:
* `IMAGEJPATH` (inside `registration.py`): path to the ImageJ executable on your computer.
* `ELASTIX_PATH` (inside elastix/run_elastix.sh): path to the elastix installation.
* Your ImageJ Input/Output settings should be set to the default values (save tiff/raw in big endian format).

Usage:
```
python registration.py -o "PATH/TO/OUTPUT/DIRECTORY" -a "PATH/TO/AUTOFLUORESCENCE/NRRD" -s "PATH/TO/SEGMENTED/CELLS/NRRD"
```

