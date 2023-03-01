###
### Script for plotting histograms of ADC values, for calibration
###

import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.optimize import curve_fit
from scipy.signal import find_peaks

from otsu import get_means

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


def gaussian(x, mu_0, a, sigma, b):
    y = (a*np.exp(-(x-mu_0)**2/(2*sigma**2))) + b

    return y


bismuth_peaks = [569.7, 1063.6] # keV

    
folder_path = "/home/hibu60/Documents/unif/unifUNIGE/lab_physics_IV/this_data/"
folder_path = "/home/hibu60/Documents/unif/unifUNIGE/lab_physics_IV/new_data/data/pmt_2/"
folder_path = "/home/hibu60/Documents/unif/unifUNIGE/lab_physics_IV/new_data/data/pmt_1/"
folder_path = "/home/massmuos/Documents/experiment/labo/data/test/"
folder_path = "/home/massmuos/Documents/experiment/labo4Muon/data/crt_data/"
#folder_path = "/home/massmuos/Documents/experiment/labo4Muon/data/data_pmt_1/"
all_files = os.listdir(folder_path)
all_files.sort()


for file in all_files:
    fig,ax = plt.subplots()
    data = np.loadtxt(folder_path + file)

    hist, bin_edges = np.histogram(data, bins=np.arange(MIN_ADC_VALUE, MAX_ADC_VALUE, 1))
    data_points = np.hstack((bin_edges[:-1].reshape(-1,1), hist.reshape(-1,1)))

    print('--------------------------------------------------------')

    ind_means = get_means(hist)
    
    guess_mu_0 = bin_edges[ind_means[0]]
    guess_mu_1 = bin_edges[ind_means[1]]
    guess_mu_2 = bin_edges[ind_means[2]]
    print('mean guesses: ', guess_mu_0, guess_mu_1, guess_mu_2)
    #guess_mu_0 = 70
    #guess_mu_1 = 120
    #guess_mu_2 = int((guess_mu_0+guess_mu_1)/2)
    guess_a_0 = hist[np.argwhere(bin_edges[:-1] >= guess_mu_0)[0]][0]
    guess_a_1 = hist[np.argwhere(bin_edges[:-1] >= guess_mu_1)[0]][0]
    guess_a_2 = hist[np.argwhere(bin_edges[:-1] >= guess_mu_2)[0]][0]
    p_init = [guess_mu_0, guess_mu_1, guess_mu_2, guess_a_0, guess_a_1, guess_a_2, 1, 1, 1, 1]

    params, covariance = curve_fit(triple_gaussian, bin_edges[:-1], hist, p0=p_init)

    print('params ', params)

    fitted_mu_0 = params[0]
    fitted_mu_1 = params[1]
    fitted_mu_2 = params[2]

    #plots gauusians/home/massmuos/Documents/experiment/labo4Muon/data/crt_data/pmt2_1753V_60mV_100k.txt
    ax.plot(bin_edges[:-1], gaussian(bin_edges[:-1], params[0], params[3], params[6], params[9]), color='red')
    ax.plot(bin_edges[:-1], gaussian(bin_edges[:-1], params[1], params[4], params[7], params[9]), color='blue')
    ax.plot(bin_edges[:-1], gaussian(bin_edges[:-1], params[2], params[5], params[8], params[9]), color='orange')

    fine_x_arr = np.linspace(MIN_ADC_VALUE, MAX_ADC_VALUE, int(1e5))
    fitted_y = triple_gaussian(fine_x_arr, *params)
    ind_peaks, _ = find_peaks(fitted_y, height=0)
    if (len(ind_peaks) < 2):
        print('Not enough peaks detected')
        if (len(ind_peaks) > 0):
            peak_0 = fine_x_arr[ind_peaks[0]]
            peak_1 = 0.
        else:
            peak_0 = 0.
            peak_1 = 0.
    else:
        peak_values = fitted_y[ind_peaks]
        ind_sorted = np.argsort(peak_values)
        ind_peaks = ind_peaks[ind_sorted]
        ind_peaks = np.flip(ind_peaks)
        peak_0 = fine_x_arr[ind_peaks[0]]
        peak_1 = fine_x_arr[ind_peaks[1]]
        
    slope = (bismuth_peaks[1] - bismuth_peaks[0]) / (peak_1 - peak_0)
    intercept = bismuth_peaks[1] - (slope*peak_1)

 
    print('filename: ', file)
    print('slope: ', slope)
    print('mu 1: ', fitted_mu_0)
    print('mu 2: ', fitted_mu_1)
    print('mu 3: ', fitted_mu_2)
    print('peak 1: ', peak_0)
    print('peak 2: ', peak_1)
    print('!!!!!!!!!!!! diff ', abs(peak_1-peak_0))
    

    ax.plot(bin_edges[:-1], hist)
    ax.plot(bin_edges[:-1], triple_gaussian(bin_edges[:-1], *params))
    #ax.hist(data, bins=300,range=[0,300] ,label=file, alpha=0.5)
    ax.set(xlabel="ADC data", ylabel="# events", title="Histogram of recorded event ({})".format(file))
    plt.legend()
    plt.savefig("pictures/" + file[:-4] + ".png")
    #plt.show()
