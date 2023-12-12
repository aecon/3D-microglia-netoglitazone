import os
import sys
import img3
import argparse


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, required=True, help="path to tif file")
    args = parser.parse_args()

    # Input tif data
    tif_path = args.i
    if os.path.isfile(tif_path)==False:
        print("File %s does not exist." % tif_path)
        sys.exit() 

    # Specify output raw and nrrd paths
    odir = os.path.dirname(tif_path)
    name = os.path.basename(tif_path)
    raw_path  = "%s/name.raw"  % (odir, name)
    nrrd_path = "%s/name.nrrd" % (odir, name)

    # Convert tif to raw/nrrd
    img3.tif2raw(tif_path, raw_path, nrrd_path)

