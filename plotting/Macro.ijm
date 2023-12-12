// Arguments:
// 1: atlas
// 2: positive
// 3: negative
// 4: outfile: merged Atlas+Neg+Pos

arg = getArgument();
arg = split(arg, ",");
atlas = arg[0];
pos = arg[1];
neg = arg[2];
out = arg[3];

// open atlas
open(atlas);
titleA = getTitle();

// open positive
open(pos);
titleP = getTitle();
selectWindow(titleP);
run("Cyan");

// open negative
open(neg);
titleN = getTitle();
selectWindow(titleN);
run("Fire");
run("Invert LUT");

// merge channels
//   c4: gray
//   c5: cyan
//   c6: magenta
cmd = "c4=" + titleA + " c5=" + titleN + " c6=" + titleP + " create"
run("Merge Channels...", cmd);
titleM = getTitle();

// fix Contrast
selectWindow(titleM);
setMinAndMax(0, 500);
selectWindow(titleM);
saveAs("Tiff", out);
titleM = getTitle();

// make montage
selectWindow(titleM);
run("Make Montage...", "columns=6 rows=5 scale=0.50");
titleMon = getTitle();
selectWindow(titleMon);
out_montage = out + "_MONTAGE.tif"
saveAs("Tiff", out_montage);
close();
