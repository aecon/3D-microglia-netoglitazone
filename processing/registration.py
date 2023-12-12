import os
import sys
import argparse

import img3


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# User settings:
#
# - Set the IMAGEJPATH below to the path to
#   the ImageJ executable on your computer.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

IMAGEJPATH = "/home/athena/Downloads/Fiji.app/ImageJ-linux64"



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Processing:
#
# - Parse user arguments for file paths.
# - Conversion of little endian raw/nrrd files
#   (output from img3), to big endian (required
#   by elastix).
# - Run elastix via system command
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-o', type=str, required=True, help="directory to store registration output")
    parser.add_argument('-a', type=str, required=True, help="path to autofluorescence data, nrrd")
    parser.add_argument('-s', type=str, required=True, help="path to segmented cells, nrrd")
    args = parser.parse_args()

    output_directory = args.o
    autofluorescence_nrrd = args.a
    segmented_nrrd = args.s

    # Conversion of img3D little endian data to big endian (necessary for elastix)
    segmented_nrrd_big_endian = segmented_nrrd + "IJ.nrrd"
    autofluorescence_nrrd_big_endian = autofluorescence_nrrd + "IJ.nrrd"

    # Generation of nrrd input for elastix, in big endian order
    basedir = os.path.abspath(os.getcwd())

    # - autofluorescence
    cmd = "%s --headless -macro imagej/save_nrrd.ijm %s,%s" % (IMAGEJPATH, (basedir+"/"+autofluorescence_nrrd), (basedir+"/"+autofluorescence_nrrd_big_endian))
    os.system(cmd)

    # - segmented
    cmd = "%s --headless -macro imagej/save_nrrd.ijm %s,%s" % (IMAGEJPATH, (basedir+"/"+segmented_nrrd), (basedir+"/"+segmented_nrrd_big_endian))
    os.system(cmd)

    # run elstix for brain registration to Allen Brain Anatomical Atlas
    cmd = "./elastix/run_elastix.sh %s %s %s" % (output_directory, autofluorescence_nrrd_big_endian, segmented_nrrd_big_endian)
    os.system(cmd)

