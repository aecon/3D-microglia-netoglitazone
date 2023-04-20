# Image pre-processing

### Data Cropping

Used to crop out large empty regions.
```
./run_crop.sh
```

### Data Flipping

Used to flip samples such that cerebellum is always on the Left.
```
python3 flip.py -i <path to nrrd file>
```


