###
### Script for plotting histograms of ADC values, for calibration
###

import numpy as np
import matplotlib.pyplot as plt
import os

folder_path = "/home/hibu60/Documents/unif/unifUNIGE/lab_physics_IV/this_data/"
all_files = os.listdir(folder_path)
fig,ax = plt.subplots()
for file in all_files:
    x = np.loadtxt(folder_path + file)
    data = x#/np.max(x)
    print(x.shape)
    ax.hist(data, bins=300,range=[0,300] ,label=file, alpha=0.5)
ax.set(xlabel="ADC data", ylabel="# events", title="Histogram of recorded event")
plt.legend()
#plt.savefig("integration.png")
plt.show()
