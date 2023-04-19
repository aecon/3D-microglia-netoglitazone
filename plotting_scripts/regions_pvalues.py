import os
import argparse
import skimage.io
import numpy as np
import pandas as pd
import adv
from scipy.stats import ttest_ind_from_stats

regions_info="regions_info.dat"
atlas_info="atlas.tab"

_data_ = pd.read_csv(atlas_info, header=None, sep='\t', lineterminator='\n')
regions_names = _data_.loc[:,3]
regions_IDs = _data_.loc[:,0]

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', type=str, nargs='+', required=True, help="Placebo  volume_per_region.dat")
    parser.add_argument('-ld', type=str, nargs='+', required=True, help="LowDose  volume_per_region.dat")
    parser.add_argument('-hd', type=str, nargs='+', required=True, help="HighDose volume_per_region.dat")
    args = parser.parse_args()

    Nregions = len(np.loadtxt(regions_info, skiprows=1))
    regions_vol = np.loadtxt(regions_info, skiprows=1, usecols=1)
    vol_p = np.zeros((Nregions, len(args.p)))
    vol_l = np.zeros((Nregions, len(args.ld)))
    vol_h = np.zeros((Nregions, len(args.hd)))

    i=0
    for p,l,h in zip(args.p, args.ld, args.hd):

        vol_p[:,i] = np.loadtxt(p, usecols=(1), skiprows=1)
        vol_l[:,i] = np.loadtxt(l, usecols=(1), skiprows=1)
        vol_h[:,i] = np.loadtxt(h, usecols=(1), skiprows=1)
        i=i+1


    mean_p = np.mean(vol_p, axis=1)
    mean_l = np.mean(vol_l, axis=1)
    mean_h = np.mean(vol_h, axis=1)
    std_p = np.std(vol_p, axis=1)
    std_l = np.std(vol_l, axis=1)
    std_h = np.std(vol_h, axis=1)

    # two-sided t-test pvalue
    ttest_l = ttest_ind_from_stats(mean1=mean_l, std1=std_l, nobs1=3, mean2=mean_p, std2=std_p, nobs2=3)
    ttest_h = ttest_ind_from_stats(mean1=mean_h, std1=std_h, nobs1=3, mean2=mean_p, std2=std_p, nobs2=3)

    # find non-nan pvalues
    condition = ((ttest_l.pvalue>0)*(ttest_l.pvalue<1)) == 1
    lstatistic = np.where( condition , ttest_l.statistic, 0)
    lpvalues   = np.where( condition , ttest_l.pvalue,    0)

    condition = ((ttest_h.pvalue>0)*(ttest_h.pvalue<1)) == 1
    hstatistic = np.where( condition , ttest_h.statistic, 0)
    hpvalues   = np.where( condition , ttest_h.pvalue,    0)

    # split effect
    leffect = np.where(lstatistic>0, +lpvalues, 0)
    leffect = np.where(lstatistic<0, -lpvalues, leffect)
    heffect = np.where(hstatistic>0, +hpvalues, 0)
    heffect = np.where(hstatistic<0, -hpvalues, heffect)

    fw = open("pvalues_regions.csv", 'w')
    fw.write("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\n " % ("Region ID", "Region name", "Region volume", "vol P1", "vol P2", "vol P3", "vol LD1", "vol LD2", "vol LD3", "vol HD1", "vol HD2", "vol HD3", "avg P", "avg LD", "avg HD", "pv LD", "pv HD") )
    for i in range(Nregions):
        fw.write("%g, %s, %g, %g, %g, %g, %g, %g, %g, %g, %g, %g, %g, %g, %g, %g, %g\n " % (regions_IDs[i], regions_names[i].replace(',', ''), regions_vol[i], vol_p[i,0], vol_p[i,1], vol_p[i,2], vol_l[i,0], vol_l[i,1], vol_l[i,2], vol_h[i,0], vol_h[i,1], vol_h[i,2], mean_p[i], mean_l[i], mean_h[i], leffect[i], heffect[i]  ) )
    fw.close()

