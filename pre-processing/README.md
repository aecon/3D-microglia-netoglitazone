# Image pre-processing

### Data Cropping

Used to crop out large empty regions.
```
./run_crop.sh
```
The upper left and bottom right corners for each sample are stored inside the file
```
corners.dat
```


### Data Flipping

Used to flip samples such that cerebellum is always on the Left.
```
python3 flip.py -i <path to nrrd file>
```


