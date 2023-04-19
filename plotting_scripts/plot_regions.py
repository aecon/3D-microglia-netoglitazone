import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats

parser = argparse.ArgumentParser()
parser.add_argument('-o', type=str, required=True, help="figure outdir")
args = parser.parse_args()

if not os.path.exists(args.o):
    os.makedirs(args.o)

#data = np.loadtxt("data_regions.dat", skiprows=1)
#    Sample         CB         HB        HPF         HY         IC         TH
data = np.loadtxt("data_regions.dat", skiprows=1, usecols=(1,2,3,4,5,6))
headers = np.loadtxt("data_regions.dat", skiprows=1, usecols=(0), dtype=str)


dx=3.26*1.e-3
dz=3.00*1.e-3
#regions = ["CB", "HB", "HPF", "HY", "IC", "TH"]
#regions = ["Cerebellum", "Brain stem", "Hippocampus", "Hypothalamus", "Cortex", "Thalamus"]
regions = ["Brain stem", "Hippocampus", "Hypothalamus", "Cortex", "Thalamus"]
vp = dx*dx*dz


Nc = np.shape(data)[1]
x_pos = np.arange(len(regions))

my_cmap = plt.cm.get_cmap('plasma')

group1=["840298_52_P_20",  "840298_16_P_17", "840298_50_P_19"]
group2=["340258_2LD_5",    "840258_3_LD_6",  "454371_17_LD_7"]
group3=["340299_35_22_HD", "840295_42_HD",   "840295_40_HD_27"]


# Compute mean/std of segmented volume per group
g1 = []
for i,s in enumerate(group1):
    idx1 = np.where(headers==s)[0]
    o = data[idx1,:][0] * vp
    g1.append( o )
means1 = np.mean(g1, axis=0)[1::]
stads1 = np.std( g1, axis=0)[1::]

g2 = []
for i,s in enumerate(group2):
    idx1 = np.where(headers==s)[0]
    o = data[idx1,:][0] * vp
    g2.append( o )
means2 = np.mean(g2, axis=0)[1::]
stads2 = np.std( g2, axis=0)[1::]

g3 = []
for i,s in enumerate(group3):
    idx1 = np.where(headers==s)[0]
    o = data[idx1,:][0] * vp
    g3.append( o )
means3 = np.mean(g3, axis=0)[1::]
stads3 = np.std( g3, axis=0)[1::]


# fig, ax = plt.subplots(figsize=(9,5))
# #ax.bar(x_pos-0.25, means1, yerr=stads1, align='edge', width=0.2, capsize=7, color='m', label="Toxofilin-Cre")
# #ax.bar(x_pos,      means2, yerr=stads2, align='edge', width=0.2, capsize=7, color='c', label="Gra16-Cre")
# #ax.bar(x_pos+0.25, means3, yerr=stads3, align='edge', width=0.2, capsize=7, color='#ffea00', label="saline")
# ax.bar(x_pos-0.25, means1, align='edge', width=0.2, edgecolor='k', linewidth=0.5, color='m', label="Control")
# ax.bar(x_pos,      means2, align='edge', width=0.2, edgecolor='k', linewidth=0.5, color='c', label="Low dose")
# ax.bar(x_pos+0.25, means3, align='edge', width=0.2, edgecolor='k', linewidth=0.5, color='#ffea00', label="High dose")
# ax.set_ylabel(r'Cell volume ($mm^3$)', fontsize=13)
# ax.set_xticks(x_pos)
# ax.set_xticklabels(regions, fontsize=13)
# ax.tick_params(axis='y', which='major', labelsize=13)
# plt.legend(prop={'size': 11})
# plt.savefig("%s/pic_per_region_counts_group_averages.png"%args.o, transparent=True)

fig, ax = plt.subplots(figsize=(9,5))
ax.bar(x_pos-0.25, means1, yerr=stads1, align='edge', width=0.2, capsize=7, edgecolor='k', linewidth=0.5, color='m', label="Control")
ax.bar(x_pos,      means2, yerr=stads2, align='edge', width=0.2, capsize=7, edgecolor='k', linewidth=0.5, color='c', label="Low dose")
ax.bar(x_pos+0.25, means3, yerr=stads3, align='edge', width=0.2, capsize=7, edgecolor='k', linewidth=0.5, color='#ffea00', label="High dose")
ax.set_ylabel(r'Cell volume ($mm^3$)', fontsize=13)
ax.set_xticks(x_pos)
ax.set_xticklabels(regions, fontsize=13)
ax.tick_params(axis='y', which='major', labelsize=13)
ax.set_ylim(bottom=0)
plt.legend(prop={'size': 11})
plt.savefig("%s/pic_per_region_counts_group_averages_w_std.png"%args.o, transparent=True)



# Compute 2-sided t-test
from scipy.stats import ttest_ind_from_stats

tCL = ttest_ind_from_stats(mean1=means2, std1=stads2, nobs1=3,   mean2=means1, std2=stads1, nobs2=3)
print("LD group", tCL)

tCH = ttest_ind_from_stats(mean1=means3, std1=stads3, nobs1=3,   mean2=means1, std2=stads1, nobs2=3)
print("HD group", tCH)




print(np.shape(g1))
print(np.shape(regions))
print(np.shape(means1))

# Dump data in CSV
fw = open("pvalues_SELECTED_regions.csv", 'w')

fw.write("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\n " % ("Region name", "vol P1", "vol P2", "vol P3", "avg_P",  "vol LD1", "vol LD2", "vol LD3", "avg_LD",  "vol HD1", "vol HD2", "vol HD3", "avg HD",  "st LD", "pv LD", "st HD", "pv HD") )

for i in range(len(means1)):
    fw.write("%s, %g, %g, %g, %g, %g, %g, %g, %g, %g, %g, %g, %g, %g, %g, %g, %g\n " % (regions[i].replace(',', ''), g1[0][i+1], g1[1][i+1], g1[2][i+1], means1[i], g2[0][i+1], g2[1][i+1], g2[2][i+1], means2[i], g3[0][i+1], g3[1][i+1], g3[2][i+1], means3[i], tCL.statistic[i], tCL.pvalue[i], tCH.statistic[i], tCH.pvalue[i] ) )

fw.close()


