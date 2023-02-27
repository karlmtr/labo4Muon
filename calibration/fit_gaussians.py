###
### Script for plotting histograms of ADC values, for calibration
###

import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.optimize import curve_fit

MIN_ADC_VALUE = 43
MAX_ADC_VALUE = 300

# Define the Gaussian function
def double_gaussian(x, mu_0, mu_1, a_0, a_1, sigma_0, sigma_1, b):
    y = ((a_0*np.exp(-(x-mu_0)**2/(2*sigma_0**2)))
         + ( a_1*np.exp(-(x-mu_1)**2/(2*sigma_1**2)))
         + b)
    return y

def triple_gaussian(x, mu_0, mu_1, mu_2, a_0, a_1, a_2, sigma_0, sigma_1, sigma_2, b):
    y = ((a_0*np.exp(-(x-mu_0)**2/(2*sigma_0**2)))
         + ( a_1*np.exp(-(x-mu_1)**2/(2*sigma_1**2)))
         + ( a_2*np.exp(-(x-mu_2)**2/(2*sigma_2**2)))
         + b)
    return y


def gaussian(x, a, x0, sigma, b):
    y = (a*np.exp(-(x-x0)**2/(2*sigma**2))) + b

    return y


bismuth_peaks = [569.7, 1063.6] # keV


folder_path = "/home/hibu60/Documents/unif/unifUNIGE/lab_physics_IV/this_data/"
folder_path = "/home/hibu60/Documents/unif/unifUNIGE/lab_physics_IV/new_data/data/pmt_2/"
folder_path = "/home/hibu60/Documents/unif/unifUNIGE/lab_physics_IV/new_data/data/pmt_1/"
all_files = os.listdir(folder_path)
all_files.sort()


for file in all_files:
    fig,ax = plt.subplots()
    data = np.loadtxt(folder_path + file)

    hist, bin_edges = np.histogram(data, bins=np.arange(MIN_ADC_VALUE, MAX_ADC_VALUE, 1))
    data_points = np.hstack((bin_edges[:-1].reshape(-1,1), hist.reshape(-1,1)))

    guess_mu_0 = 75
    guess_mu_1 = 150
    guess_mu_2 = int((guess_mu_0+guess_mu_1)/2)
    guess_a_0 = hist[np.argwhere(bin_edges[:-1] >= guess_mu_0)[0]][0]
    guess_a_1 = hist[np.argwhere(bin_edges[:-1] >= guess_mu_1)[0]][0]
    guess_a_2 = hist[np.argwhere(bin_edges[:-1] >= guess_mu_2)[0]][0]
    p_init = [guess_mu_0, guess_mu_1, guess_mu_2, guess_a_0, guess_a_1, guess_a_2, 1, 1, 1, 1]

    params, covariance = curve_fit(triple_gaussian, bin_edges[:-1], hist, p0=p_init)

    print('params ', params)

    fitted_mu_0 = params[0]
    fitted_mu_1 = params[1]
    #fitted_y_0 = triple_gaussian(fitted_mu_0, *params)
    #fitted_y_1 = triple_gaussian(fitted_mu_1, *params)

    #gm = GaussianMixture(n_components=2, random_state=0)
    #gm.fit(data_points)
    #print(gm.means_)

    #slope = (fitted_y_1 - fitted_y_0) / (fitted_mu_1 - fitted_mu_0)
    #intercept = fitted_y_1 - (slope*fitted_mu_1)

    slope = (bismuth_peaks[1] - bismuth_peaks[0]) / (fitted_mu_1 - fitted_mu_0)
    intercept = bismuth_peaks[1] - (slope*fitted_mu_1)

    #ax.plot(bin_edges[:-1], ((slope*bin_edges[:-1])+intercept), color='red')


    print('--------------------------------------------------------')
    print(file)
    print(slope)
    print('mu1', fitted_mu_0)
    print('mu2', fitted_mu_1)
    # 75, 165

    ax.plot(bin_edges[:-1], hist)
    ax.plot(bin_edges[:-1], triple_gaussian(bin_edges[:-1], *params))
    #ax.hist(data, bins=300,range=[0,300] ,label=file, alpha=0.5)
    ax.set(xlabel="ADC data", ylabel="# events", title="Histogram of recorded event ({})".format(file))
    plt.legend()
    #plt.savefig("integration.png")
    plt.show()
