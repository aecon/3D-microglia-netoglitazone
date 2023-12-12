# Image pre-processing


## Convert tif to raw/nrrd file format

* Use to convert tif files to raw/nrrd format (required for further steps of the analysis).
* After running `tif_to_raw.py` two new files will apprear inside the same folder as the original data: A `.raw` file containing the cropped data, and a corresponding `.nrrd` file containing the image metadata.

Usage:
```
python tif_to_raw.py -i "PATH/TO/TIF/FILE"
```
where "PATH/TO/TIF/FILE" is the full path to the tif file, inside quotes.




## Data Cropping

Use to crop out large empty regions, across the 3D stack.

* Generates two new files inside the same folder as the original data: a `.raw` file containing the cropped data, and a corresponding `.nrrd` file containing the image metadata. The filenames of the raw/nrrd files will be identical to the original data, prefixed with `cropped_`. 



To automate the cropping process for many brains use the script `run_crop.sh` as follows:
```
./run_crop.sh
```
**Requirements**:
* A text file containing the crop coordinates. See `corners.dat` for an example.


The upper left and bottom right corners for each sample are stored inside the file
```
corners.dat
```



## Data Flipping

Use to flip samples such that cerebellum is always on the Left.
```
python3 flip.py -i <path to nrrd file>
```


