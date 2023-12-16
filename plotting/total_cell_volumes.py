import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("data_regionsG.dat", skiprows=1, usecols=(2,3,4,5,6,7))
headers = np.loadtxt("data_regionsG.dat", skiprows=1, usecols=(1), dtype=str)
groups = np.loadtxt("data_regionsG.dat", skiprows=1, usecols=(0), dtype=str)

regions = ["Cerebellum", "Brain stem", "Hippocampus", "Hypothalamus", "Cortex", "Thalamus"]
dx=3.26*1.e-3
dz=3.00*1.e-3
vp = dx*dx*dz

sumP =np.zeros(np.shape(data)[1])
sumLD=np.zeros(np.shape(data)[1])
sumHD=np.zeros(np.shape(data)[1])
print(np.shape(sumP))

for line, group in zip(data, groups):
    if group=="P":
        sumP += line
    elif group=="LD":
        sumLD += line
    elif group=="HD":
        sumHD += line

print("Total cell volume in Placebo (mm^3):",         np.sum(sumP [1::])*vp)  #[1::] exclude cerebellum from sum
print("Total cell volume in Low Dose group (mm^3):",  np.sum(sumLD[1::])*vp)
print("Total cell volume in High Dose group (mm^3):", np.sum(sumHD[1::])*vp)

print("Regions:", regions)
print("Placebo:",  vp*sumP)
print("LowDose:",  vp*sumLD)
print("HighDose:", vp*sumHD)
