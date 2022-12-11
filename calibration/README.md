# How to use the scripts

## `linear_fits.py`

The script has  the data folder as first parameter, and the number of the PMT as a second one. It will look for files with the  following pattern : `pmt<numberPMT>_<voltage>.txt`
The script will create an image in the current directory. 

## `histograms.py`

Will plot all the distributions of the ADC count with the folder `donnee/` (for now, it's  hardcoded, but should not)

## `runCalibration.sh`

Runs the `linear_fits.py` for each PMT (from 1 to 6 now, but can be changed)and  creates a file with all the fit parameters for each PMT. 



