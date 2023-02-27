import numpy as np
import matplotlib.pyplot as plt
import glob, sys,os


if len(sys.argv) != 3 :
    print(f" USAGE : python3 {sys.argv[0]} <pathToData> <numberPMT>")
    exit(1)

filepaths = glob.glob(f"{sys.argv[1]}*")
averages = []
voltages = []
for file in filepaths:
    basename = os.path.basename(file)
    if f"pmt{sys.argv[2]}" in basename:
        data = np.loadtxt(file, unpack=True)
        #data = data[data>200]
        averages.append(np.average(data))
        voltages.append(int(basename.split("_")[-1].split(".")[0])) # takes the voltage from the filename

if len(voltages) == 0:
    print("No file associated with this PMT found, exiting...")
    exit(1)

# fit part
p = np.polyfit(voltages,averages,1)

# plot part
fig,ax = plt.subplots()
ax.plot(voltages, averages, ls="", marker="x")
x_fit = np.linspace(np.min(voltages),np.max(voltages),3)
ax.plot(x_fit, p[0]*x_fit + p[1], ls="--")
ax.set(title=f"PMT {sys.argv[2]}", xlabel="Voltage [V]", ylabel="ADC Counts")
ax.text(np.min(voltages)*1.04, np.max(averages)* (1-0.04), f"y={p[0]:.2E}x + {p[1]:.2E}" )

print(f"{sys.argv[2]},{p[0]},{p[1]}")
plt.tight_layout()
plt.savefig(f"PMT_{sys.argv[2]}.png")
