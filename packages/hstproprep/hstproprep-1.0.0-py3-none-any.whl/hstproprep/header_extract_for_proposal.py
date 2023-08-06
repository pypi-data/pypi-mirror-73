# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

import glob
from astropy.io import fits
import pandas as pd

def header_extract_for_proposal(search_path,keys_primary,keys_sci):
    ##########
    # get files
    ##########
    filelist = glob.glob(search_path)
    ##########
    # prepare table columns
    ##########
    tablelist = {}
    for i in keys_primary:
        tablelist[i] = []
    for i in keys_sci:
        tablelist[i] = []
    ##########
    # read header
    ##########
    for i in filelist:
        tmp = fits.open(i)
        for j in keys_primary:
            tablelist[j].append(tmp[0].header[j])
        for j in keys_sci:
            tablelist[j].append(tmp[1].header[j])
    return pd.DataFrame(tablelist) 
