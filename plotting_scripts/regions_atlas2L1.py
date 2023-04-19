import os
import copy
import argparse
import skimage.io
import numpy as np
import pandas as pd
import adv

fatlas_A = "/media/athena-admin/FastSSD1/Athena/atlas/ABA_25um_annotation.tif"
fregions = "atlas.tab"


def load_atlas(f):
    a = skimage.io.imread(f, plugin='tifffile').T
    return a


# load annotated regions
atlas = load_atlas(fatlas_A)
adata = pd.read_csv(fregions, header=None, sep='\t', lineterminator='\n')

lowest = adata.loc[:,0]
parent = adata.loc[:,1]
names  = adata.loc[:,3]


# atlas structure
# me    parent  name
# -1            universe
# 997   -1      brain
#


grouped = np.zeros(len(parent))
labels  = [None] * len(grouped)
i=0
fw = open("regions_level1.dat", 'w')
fw.write("%15s %15s %15s\n" % ("Original ID", "Level 1 ID", "Level 1 name"))
for l0,p0 in zip(lowest, parent):

    p = copy.deepcopy(p0)
    l = copy.deepcopy(l0)
    labels[i]  = names[i]
    grouped[i] = copy.deepcopy(l)

    print("\n")
    print("New item:")
    print("l:",l, " p:", p)
    while (p != -1) and (p!= 997):

        idx_ = np.where(lowest==p)
        assert(len(idx_)==1)
        idx = idx_[0][0]
        p_new   = copy.deepcopy(parent[idx])

        if p_new == 997:
            p = p_new
        else:
            l = copy.deepcopy(p)
            p = p_new
        
        print("l:",l, " p:", p)
        idx_ = np.where(lowest==l)
        assert(len(idx_)==1)
        idx = idx_[0][0]
        labels[i]  = names[idx]
        grouped[i] = copy.deepcopy(l)

    print("finished while group. grouped[i]=", grouped[i])
    print("region:", labels[i])

    fw.write("%15d %15d %s\n" % (l0, grouped[i], labels[i]))
    
    i = i+1

fw.close()
