import numpy as np
import pandas as pd
import pathlib
import matplotlib.pyplot as plt

pmtValues = [f"pmt{i}" for i in range(1,9)]
# pmtReg = [f"pmt_reg{i}" for i in range(1,9)]

def load_data(path : pathlib.Path) -> pd.DataFrame :
    return pd.read_csv(path, delimiter="\t", names=["time", "trigger"] + pmtValues)

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


def nbEvents_for_combinedPMTs(df:pd.DataFrame):
    """
    "Good events ?"
    ----------------
    pmt1 pmt2 pmt3 pmt4 pmt5 pmt6 pmt7 pmt8
    1    1    0    0    0    0    0    0    -> 192 (binary to decimal conversion)
    1    1    1    0    0    0    0    0    -> 224
    1    1    1    1    0    0    0    0    -> 240
    1    1    1    1    1    0    0    0    -> 248
    1    1    1    1    1    1    0    0    -> 252
    1    1    1    1    1    1    1    0    -> 254
    1    1    1    1    1    1    1    1    -> (2^8) - 1 = 255

    """
    # events that make sense ?
    event_types = [192,224, 240, 248, 252, 254, 255]
    chosen_event = event_types[-1]
    # af = df[(df["trigger"] == 192) |
    #         (df["trigger"] == 224) |
    #         (df["trigger"] == 240) |
    #         (df["trigger"] == 248) |
    #         (df["trigger"] == 252) |
    #         (df["trigger"] == 254) |
    #         (df["trigger"] == 255) 
    #         ]
    nbs = [len(df[df["trigger"] == nb]) for nb in event_types] 
    
    df = df[df["trigger"] == event_types[-1]] # We choose the event type for the ADC distribution.
    for pmtName in pmtValues: 
        fig,ax = plt.subplots()
        ax.hist(df[pmtName], bins=300, range=[0,1300])
        ax.set(xlabel="ADC", ylabel="# events", title=f"ADC distrib for {pmtName.upper()} and event type {chosen_event} ")
        # plt.show()
        plt.savefig(pathlib.Path(f"../pictures/{pmtName}_ET{chosen_event}_adc_distrib.png"))
    print(f"Wanted events\t{event_types}")
    print(f"# events\t{nbs}")


def main() :
    df = load_data(pathlib.Path("../data/2023_03_20_run_mass_muon.txt"))
    # plot_adc_distribution(df)
    # print("Number Cosmic Events", get_number_events(df, 50))
    # nbEvents_vs_th(df)
    nbEvents_for_combinedPMTs(df)


    
    
    
    
    
    




if __name__ == "__main__" :
    main()
    