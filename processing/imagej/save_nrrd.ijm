// Load nrrd from img3 and save as nrrd, with big endian order
 
arg = getArgument();
arg = split(arg, ",");
input = arg[0];
output = arg[1];

open(input);
title = getTitle();
selectWindow(title);
run("Nrrd ... ", "nrrd="+output);
close();

