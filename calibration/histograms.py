### 
### Script for plotting histograms of ADC values, for calibration
### 

import numpy as np
import matplotlib.pyplot as plt
import glob

paths = glob.glob("donnees/*")
fig,ax = plt.subplots()
for path in paths :
    name = path.split("/")[-1]
    x = np.loadtxt(path)
    print(x.shape)
    ax.hist(x, bins=100,range=[0,1000] ,label=f"{name}, N={len(x)}", alpha=0.5)
ax.set(xlabel="ADC data", ylabel="# events", title="Choix de la window pour intégrer le signal")
plt.legend()
plt.savefig("integration.png")
