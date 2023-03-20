import numpy as np
import pandas as pd
import pathlib
import matplotlib.pyplot as plt

pmtValues = [f"pmt{i}" for i in range(1,9)]
pmtReg = [f"pmt_reg{i}" for i in range(1,9)]

def load_data(path : pathlib.Path) -> pd.DataFrame :
    return pd.read_csv(path, delimiter="\t", names=pmtValues + pmtReg)

def get_number_events(df: pd.DataFrame, threshold:int = 50) -> int : 
    """
    Get the number of cosmics events, given a threshold.
    The threshold gives the adc count at which we consider it as not noise. 
    """
    filt = df[pmtValues] >= threshold
    return filt[filt.sum(axis=1) == 8].shape[0]


def plot_adc_distribution(df) :
    for pmt in pmtValues : 
        fig ,ax = plt.subplots()
        ser = df[pmt]
        ax.hist(ser, bins=300, range=[0,300], alpha=0.7)
        ax.set(xlabel="ADC data", ylabel = "# events", title=f"Recorded events {pmt}")
        plt.show()


def nbEvents_vs_th(df):
    ths = np.arange(0,1000)
    nbs = [get_number_events(df,i) for i in ths]
    plt.plot(ths,nbs) 
    plt.xlabel("threshold")
    plt.ylabel("# events")
    plt.show()
           

def main() :
    df = load_data(pathlib.Path("../data/long_run.txt"))
    plot_adc_distribution(df)
    # print("Number Cosmic Events", get_number_events(df, 50))
    # nbEvents_vs_th(df)



if __name__ == "__main__" :
    main()
    