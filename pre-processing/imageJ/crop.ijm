// https://imagej.net/scripting/macro

input = "/media/athena-admin/FastSSD1/Athena/francesca_202203/out_filter647_01/340258_2LD_5/segment/segmented.nrrd"
out00 = "/media/athena-admin/FastSSD1/Athena/crop_1.tif"
out01 = "/media/athena-admin/FastSSD1/Athena/crop_2.tif"
out10 = "/media/athena-admin/FastSSD1/Athena/crop_3.tif"
out11 = "/media/athena-admin/FastSSD1/Athena/crop_4.tif"

// load data
open(input)
title_ = getTitle()
selectWindow(title_)

// keep slices
run("Slice Keeper", "first=700 last=1100 increment=1")
saveAs("Tiff", "/media/athena-admin/FastSSD1/Athena/sliced.tif")
titleK = getTitle()

// close original image
selectWindow(title_)
close()

// duplicate and crop
tileWidth=1024
tileHeight=1024


// tile 00
selectWindow(titleK); run("Duplicate...", "title=00 duplicate"); title = getTitle(); selectWindow(title); run("Roi Defaults...")
offsetX=0
offsetY=1024
makeRectangle(offsetX, offsetY, tileWidth, tileHeight); run("Crop"); saveAs("Tiff", out00); close()

// tile 01
selectWindow(titleK); run("Duplicate...", "title=01 duplicate"); title = getTitle(); selectWindow(title); run("Roi Defaults...")
offsetX=512
offsetY=1024
makeRectangle(offsetX, offsetY, tileWidth, tileHeight); run("Crop"); saveAs("Tiff", out01); close()

// tile 10
selectWindow(titleK); run("Duplicate...", "title=10 duplicate"); title = getTitle(); selectWindow(title); run("Roi Defaults...")
offsetX=0
offsetY=512
makeRectangle(offsetX, offsetY, tileWidth, tileHeight); run("Crop"); saveAs("Tiff", out10); close()

// tile 11
selectWindow(titleK); run("Duplicate...", "title=11 duplicate"); title = getTitle(); selectWindow(title); run("Roi Defaults...")
offsetX=512
offsetY=512
makeRectangle(offsetX, offsetY, tileWidth, tileHeight); run("Crop"); saveAs("Tiff", out11); close()


