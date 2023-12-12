# Image pre-processing


## Convert tif to raw/nrrd file format

* Use to convert tif files to raw/nrrd format (**required for further steps of the analysis**).
* After running `tif_to_raw.py` two new files will apprear inside the same folder as the original data: A `.raw` file containing the cropped data, and a corresponding `.nrrd` file containing the image metadata.

Usage:
```
python tif_to_raw.py -i "PATH/TO/TIF/FILE"
```
where "PATH/TO/TIF/FILE" is the full path to the `.tif` file, inside quotes.




## Data Cropping

* Use to crop out large empty regions, across the 3D stack.
* After running `crop.py` two new files (raw/nrrd) will appear inside the same folder as the original data. The filenames of the cropped raw/nrrd files will be identical to the original data, prefixed with `cropped_`. 

Usage:
```
python crop.py -i "PATH/TO/NRRD/FILE" -x0 X0 -y0 Y0 -x1 X1 -y1 Y1
```
where "PATH/TO/NRRD/FILE" is the full path to the `.nrrd` file, and `X0, Y0, X1, Y1` are the crop coordinates:
* `X0`, `Y0`: upper left x,y pixel coordinates
* `X1`, `Y1`: lower right x,y pixel coordinates


**To automate the cropping process for many brains use the script `run_crop.sh`. Requirements**:
* `DATA`: Set the variable `DATA` in line 20 of `run_crop.sh` to the directory containing the data.
* Input data:
  * Must be in raw/nrrd format. To create raw/nrrd files from the tif files, see the section [Convert tif to raw/nrrd file format](https://github.com/aecon/3D-microglia-netoglitazone/tree/main/pre-processing#convert-tif-to-rawnrrd-file-format).
  * Filenames must be in the format `raw_SAMPLE.tif.nrrd`, where SAMPLE is the sample ID (i.e. first column in file corners.dat)
  * A file `corners.dat` containing all sample IDs and crop coordinates.

Usage:
```
./run_crop.sh
```


## Data Flipping

* Use to flip samples such that cerebellum is on the Left, and sample begins with the round part of the hemisphere, across the Z-stack. This is done to match the orientation of the Allen Brain Atlas.
* After running `flip.py` two new files (raw/nrrd) will appear inside the same folder as the original data. The filenames of the flipped raw/nrrd files will be identical to the original data, prefixed with `flip_`.

To flip the image stack horizontally, use the `-flipX` argument:
```
python3 flip.py -i "PATH/TO/NRRD/FILE" -flipX
```

To flip the image stack across the Z-direction (stack depth), use the `-flipZ` argument:
```
python3 flip.py -i "PATH/TO/NRRD/FILE" -flipZ
```

To flip both horizontally and across the Z-stack, use both arguments:
```
python3 flip.py -i "PATH/TO/NRRD/FILE" -flipX -flipZ
```




