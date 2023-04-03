# labo4Muon
## structure of the data file

- `time` : time of the event (in seconds)
- `pmts_hits` : decimal number corresponding to the trigger scheme : "00000001" means only the first PMT is triggered
- `adc_valuePMTX` : the value returned by the ADC counter for PMT X
- `tdc_valuePMTX` : the value returned by the TDC counter for PMT X

## C++ side
- ADC channels begin at 0
- TDC channels begin at 0
- HIT Scheme begin at 1 (but not really usefull to know)
